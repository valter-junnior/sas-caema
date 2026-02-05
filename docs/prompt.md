Estou criando um projeto com o seguinte escopo:

Nome: SAS - Caema, Sistema de Automação de Suporte. 

Stack principal: Python, Bat

Plataforma: Windows

Descrição: a ideia do projeto é criar um sistema que automatize algumas tarefas do setor do suporte de ti da Caema, como instlação de apps, configurações de proxy, instalação de impressora, guia de resolução de problemas para auxiliar o usuario. Como ideia inicial e mais prática quero implementar da seguinte forma: 

1. Será um app no windows 11
2. tem que iniciar junto com o sistema, e ao iniciar deve rodar um checkup de rotina
3. O app deve ter uma boa UI/UX
4. O app é dividido em duas partes:
    - um app com um menu facil e intuitivo inicialmente com duas opcoes: 
        - Rodar Checkup 
            - Nesse caso ele roda o modulo de checkup
        - Executar Solução
            - Executa o que tiver disponivel

    - modulo de checkup:
        - no modulo de checkup ele tem algums scripts no app mas com a funcao de verificar quando inicia o sistema
        - precisa ter algo visual na parte inferior direita da tela dizendo o que está execeutando no momento, nesse caso se der erro ele abre o app princial (dependendo do problema ou ele executa algo ou pede para o usuario abrir um chamado)

A primeira tarefa é criar o app visualmente e o codigo tanto do app quando da aprte do checkup que fica dentro de tudo

quero seguir um padrão de pastas da seguinte forma:
- app.py
- assets
- common/
    - views/ 
    - services/ 
- modules/
    - name_of_module/ 
        - views/
        - services/
        - batchs/

a primeira tarefa a fazer funcionar é criar um programa que ao iniciar o windows ele abra o checkup e realize a primeira tarefaa ser implementada "papel de parede"

Modulo: Papel de parede

A ideia aqui é setar por padrão o papel de parede do usuario no windwos pegando algumas informacoes como:

- Nome do usuario
- Mac e IP
- qualquer informaçlão relevante para o suporte

e tambem a imagem vai ser uma imagem que eu mesmo quero deifinir mas que tenha esse texto no canto superior direito da imagem para ficar visivel pasra o usuario (facilite no codigo para que eu consiga configurar a cor do texto facilmente caso a imagem seja escura ou branca)

a ideia aqui é facilitar para o usuario quando ele abrir um chamado e for pedido esse dados ele saber onde encontrar de maneira facil

então fazendo um checklist de tarefas:

[] criar documentação.md do projeto em /docs
[] criar todo.md do projeto em /docs ( no todo.md vai essa primeira tarefa que eu citei no caso o modulo de papel de parede)