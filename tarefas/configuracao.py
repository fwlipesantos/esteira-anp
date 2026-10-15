import os


class ConfiguracaoEsteira:
    def __init__(self):
        self.ambiente = os.getenv("ambiente", "local")
        self.sql_precos = os.getenv("pasta_sql", "../precos-anp/sql")
        self.sql_qualidade = os.getenv("pasta_sql_qualidade", "../qualidade-anp/sql")
        self.limite_atraso_horas = int(os.getenv("limite_atraso_horas", "192"))
