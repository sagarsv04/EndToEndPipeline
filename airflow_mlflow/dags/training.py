# airflow_mlflow/dags/training.py
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

def train_model():
    data = pd.read_csv("/tmp/ctr_data_processed.csv")
    X = data[['user_age', 'user_income', 'user_clicks', 'income_click_ratio']]
    y = data['ad_click']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    with mlflow.start_run():
        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)

        accuracy = clf.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)
        
        mlflow.sklearn.log_model(clf, "ctr_model")

        clf.save_model("/tmp/model.pkl")
        print(f"Model trained and saved at /tmp/model.pkl with accuracy: {accuracy}")
