FROM apache/airflow:3.1.0-python3.12

COPY esteira-anp/requirements-imagem.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY --chown=airflow:root precos-anp/anp /opt/airflow/projetos/anp
COPY --chown=airflow:root precos-anp/sql /opt/airflow/projetos/sql-precos
COPY --chown=airflow:root qualidade-anp/qualidade /opt/airflow/projetos/qualidade
COPY --chown=airflow:root qualidade-anp/sql /opt/airflow/projetos/sql-qualidade
COPY --chown=airflow:root esteira-anp/tarefas /opt/airflow/projetos/tarefas
COPY --chown=airflow:root esteira-anp/dags /opt/airflow/dags

ENV PYTHONPATH=/opt/airflow/projetos \
    pasta_sql=/opt/airflow/projetos/sql-precos \
    pasta_sql_qualidade=/opt/airflow/projetos/sql-qualidade \
    pasta_arquivos=/tmp/arquivos
