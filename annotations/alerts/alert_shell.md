# Criar Alertas pelo Cloud Shell

**Módulos:**  
1. **Definição**
2. **Alerta de erros**
3. **Alerta de Bytes**
4. **Conclusão**

## Definição
A criação de alertas pelo Cloud Shell requer o uso tanto do terminal quanto do editor de texto. Neste guia, iremos criar dois alertas: um para monitorar a ocorrência de erros nos logs do projeto e outro para acompanhar o processamento de bytes nos logs. Após a configuração dos arquivos, utilizaremos comandos no terminal do Cloud Shell para criar os alertas no sistema. Também configuraremos um Shell Script para facilitar a atualização das configurações dos alertas existentes.

## Alerta de Erros

### Criação

Para criar o alerta de erros, inicie criando um novo arquivo JSON no editor, que pode ser feito manualmente ou através de comandos no terminal:

```bash
nano alert_error.json
```

Insira o seguinte conteúdo no arquivo:

```json
{
  "displayName": "Error in logs",
  "documentation": {
    "content": "Este alerta monitora logs de erro. Um incidente é acionado imediatamente quando qualquer erro é detectado. Consulte os logs no Google Cloud Logging para mais detalhes.",
    "mimeType": "text/markdown"
  },
  "conditions": [
    {
      "displayName": "Detecção imediata de logs de erro",
      "conditionMatchedLog": {
        "filter": "severity=\"ERROR\"",
        "labelExtractors": {}
      }
    }
  ],
  "notificationChannels": [
    "projects/just-lore-435816-v8/notificationChannels/14243634302832358839"
  ],
  "combiner": "OR",
  "enabled": true,
  "alertStrategy": {
    "notificationRateLimit": {
      "period": "300s"
    }
  },
  "userLabels": {
    "severity": "error"
  }
}
```

Esse arquivo configura as especificações necessárias para o funcionamento do alerta, incluindo o nome, a documentação, as condições e os canais de notificação. O campo documentation permite a personalização do conteúdo enviado quando o alerta é acionado. O campo conditions define o filtro de logs por grau de erro. Após criar o arquivo, execute o seguinte comando para criar o alerta:

```bash
gcloud alpha monitoring policies create --policy-from-file=alert_error.json
```

### Atualização
Para atualizar o alerta já criado, crie um Shell Script que facilite a alteração das configurações:

```bash
nano update_alert_error.sh
```

Insira o seguinte conteúdo no Shell Script:

```bash
#!/bin/bash

# Variáveis para atualizar o alerta
ALERT_NAME="Error in logs"
ALERT_DOC="Este alerta monitora logs de erro. Um incidente é acionado imediatamente quando qualquer erro é detectado. Consulte os logs no Google Cloud Logging para mais detalhes."
NOTIFICATION_CHANNEL="projects/just-lore-435816-v8/notificationChannels/14243634302832358839"
USER_LABEL_SEVERITY="error"
ALERT_POLICY_ID="16832519826255041665"

# Atualizar o alerta usando gcloud
gcloud alpha monitoring policies update $ALERT_POLICY_ID \
  --display-name="$ALERT_NAME" \
  --documentation="$ALERT_DOC" \
  --documentation-format="text/markdown" \
  --set-notification-channels="$NOTIFICATION_CHANNEL" \
  --update-user-labels="severity=$USER_LABEL_SEVERITY"

# Verificação de sucesso
if [ $? -eq 0 ]; then
  echo "Política de alerta atualizada com sucesso."
else
  echo "Falha ao atualizar a política de alerta."
fi
```

Para tornar o script executável e executá-lo, use os seguintes comandos:

```bash
chmod +x update_alert_error.sh
./update_alert_error.sh
```

## Alerta de Bytes

### Criação

O processo para criar o alerta de bytes é semelhante ao anterior. Comece criando o arquivo:

```bash
nano alert_bytes.json
```

Insira o seguinte conteúdo:

```json
{
  "displayName": "Global Byte Count",
  "documentation": {
    "subject": "Alerta: Alto Contador de Bytes",
    "content": "Este alerta é acionado quando o contador de bytes para logs globais excede o limite especificado. Revise os logs para investigar possíveis problemas.",
    "mime_type": "text/markdown"
  },
  "userLabels": {
    "alert_type": "byte_count"
  },
  "conditions": [
    {
      "displayName": "Alerta de Contador de Bytes Global",
      "conditionThreshold": {
        "aggregations": [
          {
            "alignmentPeriod": "600s",
            "perSeriesAligner": "ALIGN_SUM"
          }
        ],
        "comparison": "COMPARISON_GT",
        "duration": "60s",
        "filter": "resource.type = \"global\" AND metric.type = \"logging.googleapis.com/byte_count\"",
        "thresholdValue": 500000,
        "trigger": {
          "count": 1
        }
      }
    }
  ],
  "alertStrategy": {
    "autoClose": "1800s"
  },
  "combiner": "OR",
  "enabled": true,
  "notificationChannels": [
    "projects/just-lore-435816-v8/notificationChannels/14243634302832358839",
    "projects/just-lore-435816-v8/notificationChannels/15724442209391307064"
  ],
  "severity": "WARNING"
}
```

Após criar o arquivo, execute o seguinte comando para criar o alerta:

```bash
gcloud alpha monitoring policies create --policy-from-file=alert_bytes.json
```

### Atualização

Para atualizar o alerta de bytes, crie um Shell Script semelhante:

```bash
nano update_alert_bytes.sh
```

Insira o seguinte conteúdo:

```bash
#!/bin/bash

# Variáveis para atualizar o alerta
ALERT_DISPLAY_NAME="Global Byte Count"
ALERT_SUBJECT="Alerta: Alto Contador de Bytes"
ALERT_CONTENT="Este alerta é acionado quando o contador de bytes para logs globais excede o limite especificado. Revise os logs para investigar possíveis problemas."
ALERT_TYPE="byte_count"
ALIGNMENT_PERIOD="600s"
AGGREGATION_ALIGNER="ALIGN_SUM"
COMPARISON="COMPARISON_GT"
DURATION="60s"
FILTER='resource.type = \"global\" AND metric.type = \"logging.googleapis.com/byte_count\"'
THRESHOLD_VALUE=500000
TRIGGER_COUNT=1
AUTO_CLOSE="1800s"
COMBINER="OR"
ENABLED=true
NOTIFICATION_CHANNELS=(
  "projects/just-lore-435816-v8/notificationChannels/14243634302832358839"
  "projects/just-lore-435816-v8/notificationChannels/15724442209391307064"
)
SEVERITY="WARNING"

# ID da política de alerta a ser atualizada
ALERT_POLICY_ID="3967450506088089310"

# Crie o arquivo policy_update.json
cat <<EOF > policy_update.json
{
  "displayName": "$ALERT_DISPLAY_NAME",
  "documentation": {
    "subject": "$ALERT_SUBJECT",
    "content": "$ALERT_CONTENT",
    "mime_type": "text/markdown"
  },
  "userLabels": {
    "alert_type": "$ALERT_TYPE"
  },
  "conditions": [
    {
      "displayName": "$ALERT_DISPLAY_NAME",
      "conditionThreshold": {
        "aggregations": [
          {
            "alignmentPeriod": "$ALIGNMENT_PERIOD",
            "perSeriesAligner": "$AGGREGATION_ALIGNER"
          }
        ],
        "comparison": "$COMPARISON",
        "duration": "$DURATION",
        "filter": "$FILTER",
        "thresholdValue": $THRESHOLD_VALUE,
        "trigger": {
          "count": $TRIGGER_COUNT
        }
      }
    }
  ],
  "alertStrategy": {
    "autoClose": "$AUTO_CLOSE"
  },
  "combiner": "$COMBINER",
  "enabled": $ENABLED,
  "notificationChannels": [
    $(printf '"%s",' "${NOTIFICATION_CHANNELS[@]}" | sed 's/,$//')
  ],
  "severity": "$SEVERITY"
}
EOF

# Atualizar a política de alerta usando o arquivo JSON
gcloud alpha monitoring policies update $ALERT_POLICY_ID \
  --policy-from-file="policy_update.json"

# Verificação de sucesso
if [ $? -eq 0 ]; then
  echo "Política de alerta atualizada com sucesso."
else
  echo "Falha ao atualizar a política de alerta."
fi
```

Para tornar o script executável e executá-lo, use os seguintes comandos:

```bash
chmod +x update_alert_bytes.sh
./update_alert_bytes.sh
```

Com isso, a atualização do alerta é realizada.

## Conclusão

Com base nas configurações dos arquivos por meio do Cloud Shell, foi possível configurar alertas de maneira eficiente, permitindo tanto a criação quanto a atualização de políticas de alerta diretamente via comandos, sem a necessidade de utilizar a interface gráfica do Google Cloud. Esse método proporciona maior flexibilidade e agilidade, permitindo a automação do processo de monitoramento e a criação de múltiplos alertas personalizados por meio de scripts, otimizando o gerenciamento e monitoramento de operações no Google Cloud. Assim, desenvolvedores podem utilizar soluções programáticas ao invés das interfaces visuais, ganhando mais controle e escalabilidade na configuração de alertas.