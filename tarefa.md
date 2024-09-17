# Relatórios

**Data:** 13/09/2024

## Gustavo Monteiro

### Atividades Realizadas

- Estudos sobre Cloud Monitoring e Logging, maneiras de implementar painéis de monitoramento por usuario e conta de serviço.

- Criação das primeiras Dashboards no Monitoring, inclusive a algumas bibliotecas com dashboards prontos da prórpia Google, pode ser útil posteriormente.

- Tutorial de como exportar a fatura para o Big Query.

### Resultados
- Acredito que avançamos bem duas das três requisições, como a criação de alertas e monitoramento de logs e bytes tanto por rotina como por serviço.

### Dificuldades

- Encontramos dúvidas no monitoramente do custo por usuario e contas de serviço, tentei alguma possibilidades como exportar a fatura para o Big Query e criar o painel a partir do Monitoring, gerar Query's na aba de Report's do Billing e agora criar Labels para cada membro do grupo para registrar quais serviços e custos numa tabela no Big Query, criando uma dashboard posteriormente no Monitoring.

## Luiz Otavio

### Atividades Realizadas

- Implementei o dataset do projeto com o Looker Studio

- Criei o dataset para ser mais fácil a exportação para o looker com as consultas e etc

### Resultados

Em geral acho que consegui evoluir com relação á algumas semanas atrás, porque sei que estava bem perdido em relação a todos os tópicos.

Com a ajuda dos demais integrantes da squad consegui:

- Aprender a criar datasets no Google CLoud
- Utilizar o bucket para exportar os dados para o dataset
- Entender os conceitos do Billing em geral
- Aprendi a exportar dados do Billing para o Bigquery
- Criar painéis para a análise dos logs, megabites e etc
- Entender como funciona o log e o job
- Interagir o dataset com o looker studio e aprender as ferramentas dentro dele
- Basicamente entendi como fazer rotinas e alarmes, mas acredito que ainda precise de prática para fazer sozinho


### Dúvidas 

- Mesmo procurando bastante e testando sobre, não consegui entender como implementar o painel de monitoramento de custos por usuário nominal e ainda tenho dificuldade em fazer todas as ferramentas do bigquery e billing

## Guilherme Kaneda

### Atividades Realizadas

- Desenvolvi um painel de monitoramento para acompanhar o processamento de dados (em bytes) das rotinas.

- Exportei os logs do Cloud Logging para um dataset no BigQuery.

### Resultados

- Progredimos significativamente na compreensão dos logs e jobs do ambiente GCP, além de automatizar a criação de dashboards que monitoram o processamento de bytes por dataset, rotina e no geral, utilizando o Monitoring.
- Também exportamos dados de outras APIs, como Billing e Cloud Logging, para o BigQuery, ampliando a visibilidade sobre o uso de recursos.

### Dúvidas 

- Embora tenhamos obtido bons resultados com a criação de painéis, ainda não conseguimos gerar um que mostre os custos por usuário no Monitoring, devido ao atraso na exportação completa dos dados do Billing para o BigQuery.
- Encontramos dificuldades com a API BigQuery Reservation, relacionada à mudança no modelo de cobrança de slots/hora para cobrança sob demanda.

## Guilherme Camargo Silva

### Atividades Realizadas
- Realizei a criação de alertas para o projeto, sendo utilizando logs e métricas. Criei juntamente um alerta de custos para acompanhar os valores dos projetos. Com isso se tornou fácil receber notificações personalizados de acordo com as notificações desejadas.

### Resultados
* Consegui criar alertas para acompanhar os bytes usados nos projetos, caso de erros e valor utilizado no projeto.

### Dúvidas
- Minhas dúvidas foram em certos aspectos de configuração dos alertas.

## Rafael Sinkevicius

### Atividades Realizadas

- Estudos sobre Cloud Monitoring e Logging em canais de Google Cloud.

- Criação e exploração do Looker Studio.

- Tutorial introdutório de Looker Studio.

### Resultados
- Houve um grande avanço geral, onde cada integrante entendeu pelo menos uma parte do Google Cloud.

### Dificuldades

- Houve maior dificuldade e dúvidas em exportar o Billing para o monitoramento de gastos de cada usuário.

## Henrique Fernandes Pereira (Back-end)

### Atividades Realizadas
- Estou desenvolvendo o desafio da trilha de conhecimento do Back-End.
Durante o começo para o meio da semana estava trabalhando com o Apache Fafka da Confluent, onde não estava sabendo configura-lo. Do meio para o final da semana trabalhei na API de webHook onde passaria um dado criptografado e retornaria a dado da pessoa. Próximo passo é na API WebHook realizar a mesma funcionalidade para os dados do tipo cartão e conta. Com isso realizado entra em ação o serviço de mensageria Kafka para organizar as requisições.

### Resultados
* Consegui encontrar a configuração completa para o funcionamento do Kafka para que o serviço possa ser usado no local host através do Docker-compose.
* A API WebHook está funcionando e retornando o que precisava.

### Dúvidas
- Minhas dúvidas são em relação a organização de pastas da API como projeto, porém o líder da squad de Back-End (Kelvin) perguntou na última reunião que tivemos com o desenvolvedor Matheus sobre esse assunto. Logo tirarei dúvidas com ele sobre tal necessidade.