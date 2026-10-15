# contexto do projeto

Leia este arquivo antes de qualquer alteração.

Portfólio do Felipe Santos (Data Engineer) para uma vaga de Engenheiro de Dados / DevOps: Python modular, Airflow 3, SQL avançado com Oracle, Rancher/Kubernetes on-premise, dev, hml e prod e promoção por pull request.

## os três repositórios

1. **precos-anp**: pipeline e modelo dimensional no Oracle (SCD2, MERGE, quarentena, controle de arquivos)
2. **qualidade-anp**: checagens de qualidade, alertas, monitor de atraso, fichas dos processos e laboratório de incidentes
3. **esteira-anp** (este): DAGs no Airflow 3, imagem, ambientes no Kubernetes, CI/CD e scripts de operação

Os três ficam lado a lado na mesma pasta. A imagem e o ci fazem checkout dos três.

## estilo de código

- código limpo, organizado em classes, simples de entender
- sem sintaxe complicada
- nomes em português e em minúsculo, classes com inicial maiúscula
- pouquíssimos comentários
- dags só ligam tarefas; a lógica fica nos pacotes

## estado atual

- feito: 2 dags, pacote tarefas, dockerfile, valores do helm por ambiente, oracle no cluster, 8 scripts de operação, ci e entrega no github actions, 8 testes passando com airflow 3.1 de verdade
- não testado: build da imagem, deploy no cluster e o pipeline de entrega rodando no github
