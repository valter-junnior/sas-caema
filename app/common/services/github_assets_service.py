"""Downloads catalog.csv and app installers from GitHub.

Repository: https://github.com/valter-junnior/sas-caema-apps
Files served via raw.githubusercontent.com.
"""
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

GITHUB_RAW_BASE = (
    "https://raw.githubusercontent.com/valter-junnior/sas-caema-apps/main"
)
CATALOG_FILENAME = "catalog.csv"
_USER_AGENT = "sas-caema/1.0"
_NO_CACHE_HEADERS = {
    "User-Agent": _USER_AGENT,
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}


def download_catalog(dest: Path, timeout: int = 15) -> None:
    """Download catalog.csv from GitHub and write to dest."""
    url = f"{GITHUB_RAW_BASE}/{CATALOG_FILENAME}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers=_NO_CACHE_HEADERS)
    try:
        with urlopen(req, timeout=timeout) as resp:
            dest.write_bytes(resp.read())
    except (URLError, HTTPError) as exc:
        raise RuntimeError(f"Falha ao baixar catálogo: {exc}") from exc


def download_app(
    filename: str,
    dest: Path,
    progress_callback=None,
    timeout: int = 120,
) -> None:
    """Download an app installer from GitHub and write to dest.

    progress_callback(downloaded_bytes: int, total_bytes: int) is called
    periodically if provided. total_bytes may be 0 if Content-Length is absent.
    """
    url = f"{GITHUB_RAW_BASE}/{filename}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = Request(url, headers=_NO_CACHE_HEADERS)
    try:
        with urlopen(req, timeout=timeout) as resp:
            total = int(resp.headers.get("Content-Length") or 0)
            downloaded = 0
            chunk_size = 64 * 1024  # 64 KB
            with open(dest, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)
    except (URLError, HTTPError) as exc:
        if dest.exists():
            dest.unlink()
        raise RuntimeError(f"Falha ao baixar {filename}: {exc}") from exc
