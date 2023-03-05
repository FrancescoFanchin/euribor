from requests import request
from requests.exceptions import HTTPError
import csv
import logging
import os
from time import time
from io import StringIO
import pandas as pd
from pendulum import datetime
from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    "owner": "francesco-fanchin",
    'email': None,
    "email_on_failure": False
}

connection_id = "postgres_db"


def fetch_euribor_data(ti, **kwargs):
    series_key = serieskeytoreplace
    format_type = formattoreplace
    year = kwargs["execution_date"].strftime("%Y")

    url = f"https://sdw-wsrest.ecb.europa.eu/service/data/FM/{series_key}?format={format_type}data&startPeriod={year}&endPeriod={year}"
    logging.info(url)
    try:
        response = request("GET", url)
        response.raise_for_status()

    except HTTPError as httperr:
        raise AirflowException(response.text) from httperr
    logging.info(str(response.content))

    output = response.content

    df = pd.read_csv(StringIO(output.decode("utf-8")))

    df = df[["TIME_PERIOD", "OBS_VALUE"]]
    file_path = f"/opt/airflow/data/data_{str(int(time()))}.csv"
    df.to_csv(file_path, header=False, index=False)

    ti.xcom_push(key="input_path",value=file_path)


def render_query(ti, **kwargs):
    query_path = "/opt/airflow/dags/sql/insert_data.sql"
    base_query = open(query_path).read()
    input_path=ti.xcom_pull(key='input_path', task_ids='fetch_euribor_data')
    df = pd.read_csv(input_path, header=None)
    print(df)
    lines = [f"('{df.iloc[i,0]}',{df.iloc[i,1]}),\n" for i in df.index]
    lines[-1] = lines[-1][:-2] + ";\n"
    final_query = base_query + "".join(lines)
    logging.info(final_query)
    return final_query


with DAG(
    dag_id,
    start_date=datetime(starttoreplace, 12, 1),
    end_date=datetime(endtoreplace, 12, 31),
    default_args=default_args,
    catchup=True,
    schedule_interval=scheduletoreplace,
) as dag:
    task_fetch_data = PythonOperator(
        dag=dag,
        task_id="fetch_euribor_data",
        python_callable=fetch_euribor_data,
        provide_context=True,
    )

    task_render_query = PythonOperator(
        dag=dag,
        task_id="render_query",
        python_callable=render_query,
        provide_context=True
    )
        
    task_copy_to_db = PostgresOperator(
        task_id="send_data_to_db",
        postgres_conn_id=connection_id,
        sql="{{ ti.xcom_pull(task_ids='render_query') }}",
    )

    task_fetch_data >> task_render_query >> task_copy_to_db
