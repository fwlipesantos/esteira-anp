import logging
import os
from datetime import date

from anp.baixador import Baixador
from anp.banco import Banco
from anp.carga import CargaDimensional
from anp.configuracao import Configuracao
from anp.controle import ControleArquivos
from anp.estrutura import Estrutura
from anp.leitor import LeitorArquivo
from anp.pipeline import Pipeline
from anp.tratamento import Tratamento
from anp.validacao import Validador
from qualidade.alerta import Alerta
from qualidade.monitor import MonitorAtraso
from qualidade.verificador import VerificadorQualidade
from tarefas.configuracao import ConfiguracaoEsteira

log = logging.getLogger(__name__)


class TarefasPrecosAnp:
    def __init__(self):
        self.configuracao = Configuracao()
        self.esteira = ConfiguracaoEsteira()
        self.alerta = Alerta(ambiente=self.esteira.ambiente)

    def conectar(self):
        return Banco(self.configuracao.usuario, self.configuracao.senha, self.configuracao.dsn)

    def periodo(self, params, hoje=None):
        if params.get("ano") and params.get("semestre"):
            return int(params["ano"]), int(params["semestre"])

        hoje = hoje or date.today()
        semestre = 1 if hoje.month <= 6 else 2
        return hoje.year, semestre

    def preparar_estrutura(self):
        banco = self.conectar()
        Estrutura(banco, self.esteira.sql_precos).criar()
        banco.executar_script(os.path.join(self.esteira.sql_qualidade, "estrutura", "resultado_qualidade.sql"), ignorar_existentes=True)
        banco.confirmar()

    def carregar_arquivo(self, params):
        ano, semestre = self.periodo(params)
        caminho = Baixador(self.configuracao.url_base, self.configuracao.pasta_arquivos).baixar(ano, semestre)

        banco = self.conectar()
        pipeline = Pipeline(
            leitor=LeitorArquivo(),
            tratamento=Tratamento(),
            validador=Validador(),
            banco=banco,
            controle=ControleArquivos(banco),
            carga=CargaDimensional(banco, self.esteira.sql_precos),
        )
        linhas = pipeline.processar(caminho, bool(params.get("reprocessar")))
        return {"arquivo": os.path.basename(caminho), "linhas": linhas}

    def verificar_qualidade(self, resultado_carga):
        if not resultado_carga or resultado_carga["linhas"] == 0:
            log.info("nenhuma linha nova, checagens puladas")
            return None

        verificador = VerificadorQualidade(self.conectar(), self.esteira.sql_qualidade, self.alerta)
        return verificador.executar(resultado_carga["arquivo"])

    def verificar_atraso(self):
        monitor = MonitorAtraso(self.conectar(), self.alerta)
        return monitor.verificar("precos_anp", self.esteira.limite_atraso_horas)

    def avisar_falha(self, contexto):
        self.alerta.falha(contexto)
