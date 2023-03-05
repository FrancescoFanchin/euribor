# Airflow DAG - Insert EURIBOR data

## Instructions

Generate DAG

```
python dag-generate-files.py
```
Create an empty `/data` folder at the same level of `include`.

The docker-compose.yml is taken from an official airflow example  https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml.

You can add other environment variables in the *x-airflow-common* section, such as additional pip requirements or Airflow connections.

Run Airflow with docker-compose:

```
docker-compose -f docker-compose.yml up
```
