"""Utilities to sync app/assets/apps with a mirror folder.

Commands:
- sync: Copy changed local files to mirror folder and update manifest.
- pull: Copy files from mirror folder to local folder using manifest.

This replaces cloud API dependencies with simple filesystem sync.
Use a local folder, network share, or cloud-synced folder (e.g. OneDrive).
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_APPS_DIR = ROOT_DIR / "app" / "assets" / "apps"
DEFAULT_MIRROR_DIR = ROOT_DIR / "assets_mirror"
MANIFEST_FILENAME = "manifest.json"


def _load_env_file(file_path: Path) -> None:
    """Loads KEY=VALUE pairs from a .env-style file into os.environ.

    Existing environment variables are preserved.
    """
    if not file_path.exists() or not file_path.is_file():
        return

    for raw_line in file_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("export "):
            line = line[len("export ") :].strip()

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]

        if key not in os.environ:
            os.environ[key] = value


def _load_env_files() -> None:
    """Loads local .env files from project root, if present."""
    _load_env_file(ROOT_DIR / ".env")
    _load_env_file(ROOT_DIR / ".env.local")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_files(base_dir: Path, ignored_names: set[str] | None = None) -> dict:
    files = {}
    ignored = {".gitkeep", ".gitignore", MANIFEST_FILENAME}
    if ignored_names:
        ignored.update(ignored_names)

    if not base_dir.exists():
        return files

    for item in sorted(base_dir.rglob("*")):
        if not item.is_file():
            continue
        if item.name in ignored:
            continue

        rel = item.relative_to(base_dir).as_posix()
        files[rel] = {
            "path": rel,
            "sha256": _sha256(item),
            "size": item.stat().st_size,
        }

    return files


def _build_manifest(files_map: dict, prefix: str) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prefix": prefix,
        "files": [files_map[k] for k in sorted(files_map.keys())],
    }


def _prefix_dir(mirror_dir: Path, prefix: str) -> Path:
    normalized = prefix.strip("/")
    if not normalized:
        return mirror_dir
    return mirror_dir / normalized


def _manifest_path(mirror_dir: Path, prefix: str) -> Path:
    return _prefix_dir(mirror_dir, prefix) / MANIFEST_FILENAME


def _manifest_file_path(mirror_dir: Path, prefix: str, relative_path: str) -> Path:
    return _prefix_dir(mirror_dir, prefix) / Path(relative_path)


def _load_manifest(mirror_dir: Path, prefix: str) -> dict:
    manifest_path = _manifest_path(mirror_dir, prefix)
    if not manifest_path.exists():
        return {"files": []}

    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid manifest file: {manifest_path} ({exc})") from exc


def _resolve_mirror_dir(args: argparse.Namespace) -> Path:
    env_dir = os.environ.get("ASSETS_MIRROR_DIR")
    raw_dir = args.remote_dir or env_dir or str(DEFAULT_MIRROR_DIR)
    return Path(raw_dir).expanduser().resolve()


def sync(args: argparse.Namespace) -> int:
    apps_dir = Path(args.apps_dir).resolve()
    if not apps_dir.exists():
        raise RuntimeError(f"Local assets folder not found: {apps_dir}")

    mirror_dir = _resolve_mirror_dir(args)
    prefix = os.environ.get("ASSETS_MIRROR_PREFIX", "apps")
    prefix_dir = _prefix_dir(mirror_dir, prefix)
    prefix_dir.mkdir(parents=True, exist_ok=True)

    local_files = _collect_files(apps_dir)

    remote_manifest = _load_manifest(mirror_dir, prefix)
    remote_map = {f["path"]: f for f in remote_manifest.get("files", []) if "path" in f}

    # If manifest doesn't exist yet, compare against files already present in mirror.
    if not remote_map:
        remote_map = _collect_files(prefix_dir)

    copied = 0
    skipped = 0

    for rel_path, file_info in local_files.items():
        remote_file = remote_map.get(rel_path)
        if remote_file and remote_file.get("sha256") == file_info["sha256"]:
            skipped += 1
            continue

        remote_path = _manifest_file_path(mirror_dir, prefix, rel_path)
        remote_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(apps_dir / rel_path, remote_path)
        copied += 1
        print(f"[SYNC] Copied: {rel_path}")

    deleted = 0
    if args.prune:
        local_paths = set(local_files.keys())
        remote_paths = set(remote_map.keys())
        for rel_path in sorted(remote_paths - local_paths):
            remote_path = _manifest_file_path(mirror_dir, prefix, rel_path)
            if remote_path.exists() and remote_path.is_file():
                remote_path.unlink()
                deleted += 1
                print(f"[SYNC] Deleted from mirror: {rel_path}")

        for folder in sorted(prefix_dir.rglob("*"), reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()

    manifest = _build_manifest(local_files, prefix)
    manifest_path = _manifest_path(mirror_dir, prefix)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )

    print(
        f"[SYNC] Done. copied={copied} skipped={skipped} "
        f"deleted={deleted} files={len(local_files)} mirror={prefix_dir}"
    )
    return 0


def pull(args: argparse.Namespace) -> int:
    apps_dir = Path(args.apps_dir).resolve()
    apps_dir.mkdir(parents=True, exist_ok=True)

    mirror_dir = _resolve_mirror_dir(args)
    prefix = os.environ.get("ASSETS_MIRROR_PREFIX", "apps")
    prefix_dir = _prefix_dir(mirror_dir, prefix)

    if not prefix_dir.exists():
        raise RuntimeError(f"Mirror folder not found: {prefix_dir}")

    remote_manifest = _load_manifest(mirror_dir, prefix)
    remote_files = {f["path"]: f for f in remote_manifest.get("files", []) if "path" in f}

    # Backward/fallback mode: if manifest is absent, use current mirror files.
    if not remote_files:
        remote_files = _collect_files(prefix_dir)

    if not remote_files:
        raise RuntimeError("Mirror manifest not found or empty. Run sync first.")

    copied = 0
    skipped = 0

    for rel_path, file_info in sorted(remote_files.items()):
        local_path = apps_dir / rel_path
        local_path.parent.mkdir(parents=True, exist_ok=True)

        if local_path.exists() and _sha256(local_path) == file_info.get("sha256"):
            skipped += 1
            continue

        remote_path = _manifest_file_path(mirror_dir, prefix, rel_path)
        if not remote_path.exists():
            raise RuntimeError(f"File missing in mirror: {rel_path}")

        shutil.copy2(remote_path, local_path)
        copied += 1
        print(f"[PULL] Copied: {rel_path}")

    removed = 0
    if args.prune:
        keep_paths = set(remote_files.keys())
        for item in sorted(apps_dir.rglob("*"), reverse=True):
            if item.is_file():
                rel = item.relative_to(apps_dir).as_posix()
                if item.name in {".gitkeep", ".gitignore"}:
                    continue
                if rel not in keep_paths:
                    item.unlink()
                    removed += 1
                    print(f"[PULL] Removed local extra file: {rel}")
            elif item.is_dir() and not any(item.iterdir()):
                item.rmdir()

    print(
        f"[PULL] Done. copied={copied} skipped={skipped} "
        f"removed={removed} files={len(remote_files)} mirror={prefix_dir}"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync app/assets/apps with mirror folder"
    )
    parser.add_argument(
        "--apps-dir",
        default=str(DEFAULT_APPS_DIR),
        help="Local folder to sync (default: app/assets/apps)",
    )
    parser.add_argument(
        "--remote-dir",
        default=None,
        help="Mirror base folder (or use ASSETS_MIRROR_DIR env)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_sync = subparsers.add_parser(
        "sync", help="Copy local files and manifest to mirror folder"
    )
    parser_sync.add_argument(
        "--no-prune",
        action="store_true",
        help="Do not delete mirror files that were removed locally",
    )

    parser_pull = subparsers.add_parser(
        "pull", help="Copy mirror files to local folder"
    )
    parser_pull.add_argument(
        "--no-prune",
        action="store_true",
        help="Do not delete local files that are not in mirror manifest",
    )

    return parser


def main() -> int:
    _load_env_files()

    parser = build_parser()
    args = parser.parse_args()
    args.prune = not args.no_prune

    try:
        if args.command == "sync":
            return sync(args)
        if args.command == "pull":
            return pull(args)
        parser.print_help()
        return 1
    except Exception as exc:
        print(f"[ERROR] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
