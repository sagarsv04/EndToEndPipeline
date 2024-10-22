# airflow_mlflow/dags/data_generation.py
import numpy as np
import pandas as pd

def generate_data(num_samples=10000):
    np.random.seed(42)
    data = {
        'user_id': np.random.randint(1, 1000, num_samples),
        'ad_id': np.random.randint(1, 100, num_samples),
        'user_age': np.random.randint(18, 60, num_samples),
        'user_income': np.random.randint(20000, 100000, num_samples),
        'user_clicks': np.random.randint(0, 50, num_samples),
        'ad_click': np.random.choice([0, 1], size=num_samples, p=[0.85, 0.15])
    }
    
    df = pd.DataFrame(data)
    df.to_csv("/tmp/ctr_data.csv", index=False)
    print("Data generated successfully at /tmp/ctr_data.csv")
