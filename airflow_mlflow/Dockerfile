# airflow_mlflow/Dockerfile
FROM python:3.8-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install apache-airflow==2.2.2 mlflow scikit-learn pandas flask

# Copy Airflow DAGs, Flask app, and entrypoint script
COPY dags /opt/airflow/dags/
COPY serve_model.py /opt/airflow/serve_model.py
COPY entrypoint.sh /entrypoint.sh

# Set permissions for entrypoint script
RUN chmod +x /entrypoint.sh

# Debugging: Check if the entrypoint.sh exists and has the correct permissions
RUN ls -l /entrypoint.sh

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Set the environment variable to disable example DAGs
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Expose ports for Airflow (8080), MLflow (5000), Flask API (5001)
EXPOSE 8080 5000 5001

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
