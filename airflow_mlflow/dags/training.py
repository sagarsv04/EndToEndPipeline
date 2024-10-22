# airflow_mlflow/dags/training.py
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import pickle  # Import the pickle module

def train_model():
    # Load processed data
    data = pd.read_csv("/tmp/ctr_data_processed.csv")
    X = data[['user_age', 'user_income', 'user_clicks', 'income_click_ratio']]
    y = data['ad_click']

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # Set the MLflow experiment by name (it will create the experiment if it doesn't exist)
    mlflow.set_experiment("CTR_Prediction")

    # Start an MLflow run
    with mlflow.start_run():
        clf = RandomForestClassifier()
        clf.fit(X_train, y_train)

        # Log accuracy and model
        accuracy = clf.score(X_test, y_test)
        mlflow.log_metric("accuracy", accuracy)

        # Log model to MLflow
        mlflow.sklearn.log_model(clf, "ctr_model")

        # Save model locally for deployment using pickle
        with open("/tmp/model.pkl", "wb") as f:
            pickle.dump(clf, f)  # Save the RandomForestClassifier model using pickle
        print(f"Model trained and saved at /tmp/model.pkl with accuracy: {accuracy}")
