# airflow_mlflow/Dockerfile
FROM python:3.8-slim

# Install necessary packages for building and curl
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    vim \
    libfontconfig \
    && rm -rf /var/lib/apt/lists/*

# Download and install Grafana manually
RUN curl -O https://dl.grafana.com/oss/release/grafana_8.2.5_amd64.deb \
    && dpkg -i grafana_8.2.5_amd64.deb \
    && rm grafana_8.2.5_amd64.deb

# Install Python dependencies
RUN pip install apache-airflow==2.2.2 mlflow scikit-learn pandas flask

# Install Grafana CSV plugin
RUN grafana-cli plugins install marcusolsson-csv-datasource

# Ensure provisioning folders exist for Grafana
RUN mkdir -p /etc/grafana/provisioning/dashboards

# Copy Airflow DAGs, Flask app, and entrypoint script
COPY dags /opt/airflow/dags/
COPY serve_model.py /opt/airflow/serve_model.py
COPY entrypoint.sh /entrypoint.sh
COPY grafana_dashboards /etc/grafana/provisioning/dashboards/
# Copy custom grafana.ini to enable local CSV mode
COPY grafana_dashboards/grafana.ini /etc/grafana/grafana.ini

# Set permissions for entrypoint script
RUN chmod +x /entrypoint.sh

# # Debugging: Check if the entrypoint.sh exists and has the correct permissions
# RUN ls -l /entrypoint.sh

# Create directory for CSV data for Grafana
RUN mkdir -p /opt/airflow/grafana_data

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Set the environment variable to disable example DAGs
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Expose ports for Airflow (8080), MLflow (5000), Flask API (5001), Grafana (3000)
EXPOSE 8080 5000 5001 3000

# Set entrypoint
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
