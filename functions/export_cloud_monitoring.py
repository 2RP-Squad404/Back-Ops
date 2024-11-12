import google.auth
import google.auth.transport.requests
import requests
from google.cloud import bigquery
from datetime import datetime, timedelta, timezone

project_id = "just-lore-435816-v8"

end_time = (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

url = "https://monitoring.googleapis.com/v3/projects/just-lore-435816-v8/timeSeries"
# Exportação dos bytes logs global
params = {
    "interval.startTime": "2024-09-17T00:00:00.000000Z", 
    "interval.endTime": end_time,  
    "aggregation.alignmentPeriod": "60s",
    "aggregation.perSeriesAligner": "ALIGN_SUM", 
    "aggregation.crossSeriesReducer": "REDUCE_SUM",  
    "filter": 'metric.type="logging.googleapis.com/byte_count" resource.type="global"',
    "aggregation.groupByFields": "metric.labels.key"
}

credentials, _ = google.auth.default()
auth_request = google.auth.transport.requests.Request()

# Atualiza o token de acesso
credentials.refresh(auth_request)
auth_token = credentials.token

headers = {"Authorization": f"Bearer {auth_token}"}

# Requisição HTTP
response = requests.get(url, headers=headers, params=params)

# Carrega a resposta JSON
data = response.json()

# Se 'data' não é uma lista, você pode precisar convertê-lo em uma lista.
if not isinstance(data, list):
    data = [data]  

client = bigquery.Client(project=project_id)

dataset_id = 'metrics'
table_id = 'byte_count_global'
table_ref = client.dataset(dataset_id).table(table_id)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)

# Aguarda a conclusão
load_job.result()

# Exportação dos bytes logs dataset
params = {
    "interval.startTime": "2024-09-17T00:00:00.000000Z", 
    "interval.endTime": end_time,  
    "aggregation.alignmentPeriod": "60s",
    "aggregation.perSeriesAligner": "ALIGN_SUM", 
    "aggregation.crossSeriesReducer": "REDUCE_SUM",  
    "filter": 'metric.type="logging.googleapis.com/byte_count" resource.type="bigquery_dataset"',
    "aggregation.groupByFields": "metric.labels.key"
}

# Requisição HTTP
response = requests.get(url, headers=headers, params=params)

# Carrega a resposta JSON
data = response.json()

# Se 'data' não é uma lista, você pode precisar convertê-lo em uma lista.
if not isinstance(data, list):
    data = [data]  

table_id = 'byte_count_dataset'
table_ref = client.dataset(dataset_id).table(table_id)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)

# Aguarda a conclusão
load_job.result()

# Exportação dos bytes logs routine
params = {
    "interval.startTime": "2024-09-17T00:00:00.000000Z", 
    "interval.endTime": end_time,  
    "aggregation.alignmentPeriod": "60s",
    "aggregation.perSeriesAligner": "ALIGN_SUM", 
    "aggregation.crossSeriesReducer": "REDUCE_SUM",  
    "filter": 'metric.type="logging.googleapis.com/byte_count" resource.type="dataform.googleapis.com/Repository"',
    "aggregation.groupByFields": "metric.labels.key"
}

# Requisição HTTP
response = requests.get(url, headers=headers, params=params)

# Carrega a resposta JSON
data = response.json()

# Se 'data' não é uma lista, você pode precisar convertê-lo em uma lista.
if not isinstance(data, list):
    data = [data]  

table_id = 'byte_count_routine'
table_ref = client.dataset(dataset_id).table(table_id)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)

# Aguarda a conclusão
load_job.result()