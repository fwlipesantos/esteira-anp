from datetime import date

from tarefas.precos_anp import TarefasPrecosAnp


def test_periodo_vem_dos_parametros():
    assert TarefasPrecosAnp().periodo({"ano": 2023, "semestre": 2}) == (2023, 2)


def test_periodo_padrao_e_o_semestre_atual():
    tarefas = TarefasPrecosAnp()
    assert tarefas.periodo({}, hoje=date(2024, 3, 10)) == (2024, 1)
    assert tarefas.periodo({}, hoje=date(2024, 9, 10)) == (2024, 2)


def test_sem_linhas_novas_nao_verifica_qualidade():
    assert TarefasPrecosAnp().verificar_qualidade({"arquivo": "x.csv", "linhas": 0}) is None
