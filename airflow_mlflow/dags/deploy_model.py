# airflow_mlflow/dags/deploy_model.py
import shutil

def deploy_model():
    shutil.copy("/tmp/model.pkl", "/opt/airflow/model.pkl")
    print("Model deployed at /opt/airflow/model.pkl")
