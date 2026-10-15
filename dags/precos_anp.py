from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG, Param

from tarefas.precos_anp import TarefasPrecosAnp

tarefas = TarefasPrecosAnp()


def preparar_estrutura():
    tarefas.preparar_estrutura()


def carregar_arquivo(params):
    return tarefas.carregar_arquivo(params)


def verificar_qualidade(ti):
    resultado = ti.xcom_pull(task_ids="carregar_arquivo")
    tarefas.verificar_qualidade(resultado)


padrao = {
    "owner": "felipe",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "on_failure_callback": tarefas.avisar_falha,
}

with DAG(
    dag_id="precos_anp",
    description="carrega os precos de combustiveis da anp no modelo dimensional do oracle",
    schedule="0 6 * * 1",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args=padrao,
    tags=["anp", "oracle"],
    params={
        "ano": Param(None, type=["null", "integer"]),
        "semestre": Param(None, type=["null", "integer"], enum=[None, 1, 2]),
        "reprocessar": Param(False, type="boolean"),
    },
) as dag:
    tarefa_estrutura = PythonOperator(task_id="preparar_estrutura", python_callable=preparar_estrutura)
    tarefa_carga = PythonOperator(task_id="carregar_arquivo", python_callable=carregar_arquivo, execution_timeout=timedelta(minutes=60))
    tarefa_qualidade = PythonOperator(task_id="verificar_qualidade", python_callable=verificar_qualidade, retries=0)

    tarefa_estrutura >> tarefa_carga >> tarefa_qualidade
