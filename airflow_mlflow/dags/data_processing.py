import pandas as pd
import os
from scipy.stats import ks_2samp

# Log data statistics
def log_data_statistics(df, stage_name):
    stats = df.describe().T
    stats['missing_values'] = df.isnull().sum()
    
    if not os.path.exists("/opt/airflow/grafana_data/"):
        os.makedirs("/opt/airflow/grafana_data/")
    file_path = f"/opt/airflow/grafana_data/{stage_name}_stats.csv"
    stats.to_csv(file_path)
    print(f"Logged statistics for {stage_name} data at {file_path}")

# Detect data drift
def detect_data_drift(new_data, historical_data):
    # new_data = pd.read_csv(new_data_path)
    # historical_data = pd.read_csv(historical_data_path)
    drift_report = {}
    for col in ['user_age', 'user_income', 'user_clicks', 'income_click_ratio']:
        stat, p_value = ks_2samp(new_data[col], historical_data[col])
        drift_report[col] = p_value

    drift_df = pd.DataFrame(list(drift_report.items()), columns=['feature', 'p_value'])
    drift_df.to_csv("/opt/airflow/grafana_data/drift_report.csv", index=False)
    print("Data drift detection report saved to /opt/airflow/grafana_data/drift_report.csv")

def process_data():
    # Read the current batch of data
    data = pd.read_csv("/opt/airflow/tmp/ctr_data.csv")
    data['income_click_ratio'] = data['user_income'] / (data['user_clicks'] + 1)
    
    # Detect data drift by comparing the current batch with historical data (if it exists)
    try:
        old_data = pd.read_csv("/opt/airflow/tmp/ctr_data_processed.csv")
        # Save the current batch as the historical data for future comparison
        log_data_statistics(old_data, 'historical')
        
        # Log statistics for the new data
        log_data_statistics(data, 'new')
        
        # detect_data_drift("/opt/airflow/grafana_data/new_stats.csv", "/opt/airflow/grafana_data/historical_stats.csv")
        detect_data_drift(data, old_data)
    except FileNotFoundError:
        print("No historical data found. Skipping data drift detection for the first run.")
    
    if not os.path.exists("/opt/airflow/tmp/"):
        os.makedirs("/opt/airflow/tmp/")
    # Save processed data
    data.to_csv("/opt/airflow/tmp/ctr_data_processed.csv", index=False)
    print("Processed data saved at /opt/airflow/tmp/ctr_data_processed.csv")
