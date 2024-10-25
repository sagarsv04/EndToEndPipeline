# EndToEndPipeline
## CTR Prediction System with Airflow, MLflow, Docker, and Flask

This project demonstrates an end-to-end machine learning pipeline for **Click-Through Rate (CTR) Prediction**. The pipeline includes data generation, data processing, model training, and model deployment using **Airflow** as the orchestrator and **MLflow** for tracking experiments. The trained model is served using a **Flask API** for real-time predictions.

## Project Structure
```
EndToEndPipeline/
├── airflow_mlflow/
│   ├── dags/
│   │   ├── ctr_pipeline.py          # Main Airflow pipeline (DAG)
│   │   ├── data_generation.py       # Synthetic data generation
│   │   ├── data_processing.py       # Data processing and feature engineering
│   │   ├── training.py              # Model training and MLflow logging
│   │   └── deploy_model.py          # Model deployment logic
│   ├── serve_model.py               # Flask API for serving the trained model
│   ├── Dockerfile                   # Dockerfile for building the environment
│   └── entrypoint.sh                # Entrypoint script to start all services
├── grafana_dashboards/
│   └── ctr_dashboard.json            # Pre-configured Grafana dashboard
├── grafana_data/                     # CSVs for Grafana visualization
│   ├── historical_stats.csv          # Historical data distribution stats
│   └── new_stats.csv                 # New data distribution stats
├── kubernetes/
│   ├── combined_deployment.yaml     # Kubernetes deployment for Airflow + MLflow + Flask
│   └── service.yaml                 # Kubernetes service definition
└── README.md                        # Documentation
```

## Prerequisites
- Docker
- Docker Compose (Optional, if using locally)
- Kubernetes (Optional, if deploying on Kubernetes)
- Python 3.8 (apache-airflow==2.2.2, mlflow, scikit-learn, pandas, flask)

## Steps to Run Locally with Docker
### Clone the Repository
```
git clone <repository-url>
cd EndToEndPipeline/airflow_mlflow/
```
### Build the Docker Image
```
docker build -t ctr-combined .
```
### Run the Docker Container
```
docker run -p 8080:8080 -p 5000:5000 -p 5001:5001 -p 3000:3000 ctr-combined
```
- Airflow UI will be available at http://localhost:8080
- MLflow UI will be available at http://localhost:5000
- Grafana UI will be available at http://localhost:3000
- Flask API for model predictions will be available at http://localhost:5001

### Access Airflow and Trigger the DAG
```
- Go to http://localhost:8080.
- Log in using the default Airflow credentials:
- - Username: admin
- - Password: admin
- Trigger the ctr_pipeline DAG from the Airflow UI.
This will:
- - Generate synthetic data.
- - Process the data.
- - Train a RandomForest model.
- - Log the experiment in MLflow.
- - Deploy the trained model for use with the Flask API.
```

### Test the Flask API
```
curl -X POST http://localhost:5001/predict \
-H "Content-Type: application/json" \
-d '[
    {
        "user_age": 30,
        "user_income": 50000,
        "user_clicks": 10,
        "income_click_ratio": 5000
    },
    {
        "user_age": 40,
        "user_income": 60000,
        "user_clicks": 15,
        "income_click_ratio": 4000
    }
]'

```

## Apply Kubernetes Deployment
- Go to the kubernetes/ directory and apply the deployment and service:
```
kubectl apply -f combined_deployment.yaml
kubectl apply -f service.yaml
```
- Access the Services
```
kubectl get services
```
- Airflow UI will be available at http://external_ip:8080
- MLflow UI will be available at http://external_ip:5000
- Grafana UI will be available at http://external_ip:3000
- Flask API will be available at http://external_ip:5001

## WIP
- Grafana doesn't auto-load csv files and require manual panel setup