# airflow_mlflow/dags/data_processing.py
import pandas as pd

def process_data():
    data = pd.read_csv("/tmp/ctr_data.csv")
    data['income_click_ratio'] = data['user_income'] / (data['user_clicks'] + 1)
    data.to_csv("/tmp/ctr_data_processed.csv", index=False)
    print("Data processed and saved at /tmp/ctr_data_processed.csv")
