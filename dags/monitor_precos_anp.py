from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG

from tarefas.precos_anp import TarefasPrecosAnp

tarefas = TarefasPrecosAnp()


def verificar_atraso():
    tarefas.verificar_atraso()


with DAG(
    dag_id="monitor_precos_anp",
    description="avisa quando a carga de precos da anp esta atrasada",
    schedule="0 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    default_args={"owner": "felipe", "retries": 1, "retry_delay": timedelta(minutes=2)},
    tags=["anp", "monitoramento"],
) as dag:
    PythonOperator(task_id="verificar_atraso", python_callable=verificar_atraso)
