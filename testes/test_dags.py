import os

import pytest

pasta_dags = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dags")


@pytest.fixture(scope="module")
def dagbag():
    from airflow.models import DagBag

    return DagBag(dag_folder=pasta_dags, include_examples=False)


def test_dags_carregam_sem_erro(dagbag):
    assert dagbag.import_errors == {}


def test_dags_esperadas(dagbag):
    assert set(dagbag.dag_ids) == {"precos_anp", "monitor_precos_anp"}


def test_ordem_das_tarefas(dagbag):
    dag = dagbag.dags["precos_anp"]
    assert dag.get_task("preparar_estrutura").downstream_task_ids == {"carregar_arquivo"}
    assert dag.get_task("carregar_arquivo").downstream_task_ids == {"verificar_qualidade"}


def test_todas_as_dags_tem_retry_e_dono(dagbag):
    for dag in dagbag.dags.values():
        for tarefa in dag.tasks:
            assert tarefa.owner == "felipe"
        assert dag.default_args.get("retries", 0) >= 1


def test_todas_as_dags_tem_ficha():
    pasta_fichas = os.path.join(os.path.dirname(pasta_dags), "..", "qualidade-anp", "processos")
    fichas = {nome.replace(".yml", "") for nome in os.listdir(pasta_fichas)}
    dags = {nome.replace(".py", "") for nome in os.listdir(pasta_dags) if nome.endswith(".py")}
    assert dags <= fichas
