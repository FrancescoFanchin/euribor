# Airflow DAG - Insert EURIBOR data

## Instructions

Generate DAG

```
python dag-generate-files.py
```

Run Airflow with docker-compose (Found an official example at https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml):

```
docker-compose -f docker-compose.yml up
```