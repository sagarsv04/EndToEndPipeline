# airflow_mlflow/dags/ctr_pipeline.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from data_generation import generate_data
from data_processing import process_data
from training import train_model
from deploy_model import deploy_model

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

dag = DAG('ctr_pipeline', default_args=default_args, schedule_interval='@daily')

generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag
)

process_data_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

deploy_model_task = PythonOperator(
    task_id='deploy_model',
    python_callable=deploy_model,
    dag=dag
)

generate_data_task >> process_data_task >> train_model_task >> deploy_model_task
