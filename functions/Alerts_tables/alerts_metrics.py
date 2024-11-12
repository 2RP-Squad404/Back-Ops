from google.cloud import monitoring_v3, bigquery
import json

project_id = "integracaohomologado"
project_name = f"projects/{project_id}"
table_id = f"{project_id}.alerts.metrics"

# Encontra os emails não cadastrados como canal na tabela
client_monitoring = monitoring_v3.NotificationChannelServiceClient()
client_bigquery = bigquery.Client(project=project_id)

# recupera os canais de notificação
channels = client_monitoring.list_notification_channels(name=project_name)

emails_alertas = []

# Itera pelos canais e extrai os emails
for channel in channels:
    if channel.type_ == "email":
        emails_alertas.append(channel.labels["email_address"])

# consulta para extrair os emails
query = f"""
    SELECT email
    FROM `{table_id}`
"""
query_job = client_bigquery.query(query)

# resultado da consulta
results = query_job.result()
emails_bigquery = list([row.email for row in results])

# verificando se os emails da tabela existem nos emails de alertas e evita repetições (set)
emails_faltantes = list({email for email in emails_bigquery if email not in emails_alertas})

# -------------------------------------------------------------------------------------------------
# Cadastro o email como um canal

if emails_faltantes:
    print("E-mails faltantes nos alertas:", emails_faltantes)
    
    # para cada email faltante, cria um canal de notificação
    for email in emails_faltantes:
        display_name = f"Alerta para {email}"
        description = f"Canal de notificação para {email}"
        
        # comando para criar o canal de notificação
        notification_channel = monitoring_v3.NotificationChannel(
            type_="email",
            display_name=display_name,
            description=description,
            labels={"email_address": email},
        )

        # Cria o canal de notificação
        response = client_monitoring.create_notification_channel(request={"name": project_name, "notification_channel": notification_channel})

        print(f"Canal de notificação criado: {response.name}")
else:
    print("Todos os emails já estão configurados.")

# --------------------------------------------------------------------------------------------------------
# Adiciona os id dos emails cadastrados na tabela

# recupera o ID de um email
def get_alert_channel_id(email):
    channels = client_monitoring.list_notification_channels(name=project_name)
    for channel in channels:
        if channel.labels.get('email_address') == email:
            return channel.name.split('/')[-1]

# atualiza os ID de todos os emails na tabela
for email in emails_bigquery:
    alert_channel_id = get_alert_channel_id(email)

    print(alert_channel_id)

    query = f"""
    UPDATE `{table_id}`
    SET id_email = '{alert_channel_id}'
    WHERE email = '{email}'
    """

    query_job = client_bigquery.query(query)
    query_job.result()

    print("Elemento atualizado com sucesso.")

# ----------------------------------------------------------------------------------------
# Criação de alertas pela tabela

client_monitoring = monitoring_v3.AlertPolicyServiceClient()

with open('alert_metric.json', 'r') as f:
    json_metric = json.load(f)

query = f"SELECT * FROM `{table_id}`"
query_job = client_bigquery.query(query)
rows = query_job.result()

for row in rows:
    # cria um alerta de metrica a partir dessa linha
    json_metric["display_name"] = row.alert_name
    json_metric["conditions"][0]["condition_threshold"]["filter"] = f'resource.type = \"{row.resource}\" AND metric.type = \"{row.metric}\"'
    json_metric["conditions"][0]["condition_threshold"]["threshold_value"] = int(row.limitation)
    json_metric["notification_channels"] = [f'{project_name}/notificationChannels/{row.id_email}']

    print("JSON de metrica alterado")

    alert_policy = client_monitoring.create_alert_policy(name = project_name, alert_policy = json_metric)
    # Extrai o ID da política de alerta criada
    alert_policy_id = alert_policy.name.split('/')[-1]
    
    query = f"""
    UPDATE `{table_id}`
    SET alert_id = '{alert_policy_id}'
    WHERE alert_name = '{row.alert_name}' AND metric = '{row.metric}' AND id_email = '{row.id_email}'
    """

    print(f'Alerta de Metrica criado para a linha: {row}')
    
    query_job = client_bigquery.query(query)
    query_job.result()
    
print("Processo de criação de alertas concluído.")

# ----------------------------------------------------------------------------------------
# lista as politicas de alerta
policies = client_monitoring.list_alert_policies(name=project_name)

query = f"SELECT * FROM `{table_id}`"

# executa a query
query_job = client_bigquery.query(query)
rows = query_job.result()

# Lista as linhas
rows = list(rows)

for policy in policies:
    # Verifique se o alerta não está em nenhuma linha e se tem a condição 'condition_matched_log'
    if (policy.name not in [f'{project_name}/alertPolicies/{r.alert_id}' for r in rows] and any('condition_matched_log' not in condition for condition in policy.conditions)):
        # Exclui os alertas
        try:
            client_monitoring.delete_alert_policy(name=policy.name)
            print(f"Excluída a política de alerta: {policy.name}")
        except:
            print(f"Erro ao excluir a política de alerta {policy.name}")
                
print("Processo de exclusão de alertas concluído.")