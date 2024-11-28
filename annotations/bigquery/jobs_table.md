# Tabela dos Jobs

**Módulos:**  
1. **Definição**
2. **Exportação do JOBS_BY_PROJECT**
3. **Simplicar criação da tabela**

## Definição
A tabela JOBS_BY_PROJECT do INFORMATION_SCHEMA do BigQuery fornece informações detalhadas sobre os jobs (tarefas) que foram executados em um determinado projeto no Google BigQuery. Assim, salvaremos em uma tabela particionada em nosso BigQuery, para uma melhor visualização.

## Exportação do JOBS_BY_PROJECT

A partir de um script SQL, é possível criar uma tabela em dataset com todas as informações da JOBS_BY_PROJECT.

```sql
CREATE OR REPLACE TABLE just-lore-435816-v8.billing.jobs
SELECT *
FROM region-southamerica-east1.INFORMATION_SCHEMA.JOBS_BY_PROJECT
```

### Adição de colunas

Porém, além de criar ela, devemos adicionar uma coluna de preço para cada job. Como base, usamos a [documentaçao do BigQuery](https://cloud.google.com/bigquery/pricing?hl=pt-br).

Ou seja, para cada TB gasto, R$64,00 serão cobrados. Portanto, devemos converter o total de bytes gasto em TB, divindo-o por 10^12 e, por fim, multiplicando por 64.

```sql
CREATE OR REPLACE TABLE just-lore-435816-v8.billing.jobs
PARTITION BY DATE(creation_time) AS
SELECT 
  *,
  (total_bytes_billed / POW(10, 12)) * 64 AS price
FROM region-southamerica-east1.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE total_bytes_billed > 0
```

Além disso, é essencial o particionamento da tabela. Para isso, utilizamos a coluna creation_time, na qual seu tipo de dado é DATE.

## Simplicar criação da tabela

Como devemos manter atualizada essa tabela, uma rotina no DataForm para sua recriação seria custosa, logo, criamos um script SQLX do tipo incremental.

```sql
config {
   type: "incremental",
    database: "integracaohomologado",
    schema: "billing",
    name: "jobs",
}

WITH routine AS (
  SELECT 
    parent.parent_job_id AS routine_parent_job_id, 
    parent_label.value AS routine
  FROM region-southamerica-east1.INFORMATION_SCHEMA.JOBS_BY_PROJECT AS parent
  CROSS JOIN UNNEST(parent.labels) AS parent_label
  WHERE parent_label.key = 'routine'
  GROUP BY parent.parent_job_id, parent_label.value 
)

SELECT 
  jobs.*,
  (jobs.total_bytes_billed / POW(10, 12)) * 64 AS price,
  (SELECT value FROM UNNEST(jobs.labels) WHERE key = 'dataform_repository_id') AS dataform_repository,
  routine.routine AS routine
FROM region-southamerica-east1.INFORMATION_SCHEMA.JOBS_BY_PROJECT AS jobs
LEFT JOIN routine 
  ON routine.routine_parent_job_id = jobs.job_id
WHERE jobs.total_bytes_billed > 0 AND job_id NOT IN (SELECT job_id FROM integracaohomologado.billing.jobs)
```

Devemos adicionar somente as linhas que não estão na tabela. 

```sql
WHERE job_id NOT IN (SELECT job_id FROM integracaohomologado.billing.jobs)
```