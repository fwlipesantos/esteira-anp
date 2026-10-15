# operação

Tarefas do dia a dia no cluster, sempre por script e nunca editando recurso na mão.

## subir um ambiente do zero

```bash
cp .env.exemplo .env.dev          # preencher com os valores do ambiente
./scripts/subir_ambiente.sh dev   # namespace, segredo e oracle
./scripts/deploy.sh dev latest    # airflow com a imagem escolhida
```

## publicar uma versão

O caminho normal é pelo pipeline de entrega. Manualmente, só em emergência e com registro na tarefa:

```bash
./scripts/deploy.sh hml a1b2c3d
```

## voltar uma versão

```bash
./scripts/rollback.sh prod
```

Volta para a versão anterior do helm. O histórico das últimas cinco aparece antes do rollback.

## trocar variável ou segredo

1. editar o `.env.<ambiente>` (nunca vai para o git)
2. aplicar e reiniciar de forma controlada:

```bash
./scripts/segredos.sh hml
./scripts/reiniciar.sh hml
```

## consultar logs

```bash
./scripts/logs.sh prod scheduler
./scripts/logs.sh prod dag-processor
```

O log de cada tarefa fica na interface do Airflow. Com o KubernetesExecutor, cada tarefa roda num pod próprio:

```bash
./scripts/status.sh prod
kubectl -n airflow-prod describe pod <pod-da-tarefa>
```

## investigar uma carga no oracle

```sql
-- situação de cada arquivo
select arquivo, status, linhas, rejeitadas, duplicadas, inicio, fim, mensagem
from controle_arquivo
order by inicio desc

-- motivos de rejeição
select motivo, count(*) from rejeitado_preco where arquivo = :arquivo group by motivo

-- resultado das checagens de qualidade
select checagem, severidade, problemas, aprovado
from resultado_qualidade
where arquivo = :arquivo
order by verificado_em desc
```

## reiniciar sem derrubar execuções

`./scripts/reiniciar.sh` reinicia um componente por vez e espera cada um voltar antes de seguir. As tarefas em andamento continuam nos seus próprios pods.
