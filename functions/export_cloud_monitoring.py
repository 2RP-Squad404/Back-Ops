import google.auth
import google.auth.transport.requests
import requests
from google.cloud import bigquery
from datetime import datetime, timedelta, timezone

project_id = "integracaohomologado"

end_time = (datetime.now(timezone.utc) - timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

url = "https://monitoring.googleapis.com/v3/projects/integracaohomologado/timeSeries"
# Exportação dos bytes logs global
params = {
    "interval.startTime": "2024-10-24T00:00:00.000000Z", 
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
data = response.json()

# Se 'data' não é uma lista, você pode precisar convertê-lo em uma lista.
if isinstance(data, dict):
    data = [data]  

client = bigquery.Client(project=project_id)

dataset_id = 'billing'
table_id = 'byte_count_global'
table_ref = client.dataset(dataset_id).table(table_id)

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)
load_job.result()

#----------------------------------------------------------------------------------------------------------
# Exportação dos bytes logs dataset
params = {
    "interval.startTime": "2024-10-24T00:00:00.000000Z", 
    "interval.endTime": end_time,  
    "aggregation.alignmentPeriod": "60s",
    "aggregation.perSeriesAligner": "ALIGN_SUM", 
    "aggregation.crossSeriesReducer": "REDUCE_SUM",  
    "filter": 'metric.type="logging.googleapis.com/byte_count" resource.type="bigquery_dataset"',
    "aggregation.groupByFields": "resource.label.\"dataset_id\""
}

# Requisição HTTP
response = requests.get(url, headers=headers, params=params)
data = response.json()

# Se 'data' não é uma lista, você pode precisar convertê-lo em uma lista.
if isinstance(data, dict):
    data = [data]  

table_id = 'byte_count_dataset'
table_ref = client.dataset(dataset_id).table(table_id)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)
load_job.result()

#----------------------------------------------------------------------------------------------------------
# Exportação dos bytes logs severity
params = {
    "interval.startTime": "2024-10-24T00:00:00.000000Z",
    "interval.endTime": end_time,
    "aggregation.alignmentPeriod": "60s",
    "aggregation.perSeriesAligner": "ALIGN_SUM",
    "aggregation.crossSeriesReducer": "REDUCE_SUM",
    "filter": 'metric.type="logging.googleapis.com/log_entry_count" resource.type="global"',
    "aggregation.groupByFields": "metric.label.severity"
}

# Requisição HTTP
response = requests.get(url, headers=headers, params=params)
data = response.json()

if isinstance(data, dict):
    data = [data]  

table_id = 'log_severity'
table_ref = client.dataset(dataset_id).table(table_id)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)
load_job.result()

#----------------------------------------------------------------------------------------------------------
# Exportação dos bytes logs do Dataform
params = {
    "interval.startTime": "2024-10-24T00:00:00.000000Z",
    "interval.endTime": end_time,
    "aggregation.alignmentPeriod": "60s",
    "aggregation.perSeriesAligner": "ALIGN_SUM",
    "aggregation.crossSeriesReducer": "REDUCE_SUM",
    "filter": 'metric.type="logging.googleapis.com/byte_count" resource.type="dataform.googleapis.com/Repository"',
    "aggregation.groupByFields": "resource.label.repository_id"
}

# Requisição HTTP
response = requests.get(url, headers=headers, params=params)
data = response.json()

if isinstance(data, dict):
    data = [data]  

table_id = 'byte_count_dataform'
table_ref = client.dataset(dataset_id).table(table_id)

# Exporta para a tabela
load_job = client.load_table_from_json(data, table_ref, job_config=job_config)

# Aguarda a conclusão
load_job.result()
