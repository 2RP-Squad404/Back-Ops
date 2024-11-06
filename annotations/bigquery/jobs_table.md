# Tabela dos Jobs

**Módulos:**  
1. **Definição**
2. **Exportação do JOBS_BY_PROJECT**
3. **Simplicar criação da tabela**

## Definição
A tabela JOBS_BY_PROJECT do INFORMATION_SCHEMA do BigQuery fornece informações detalhadas sobre os jobs (tarefas) que foram executados em um determinado projeto no Google BigQuery. Assim, salvaremos em uma tabela particionada em nosso BigQuery, para uma melhor visualização.

## Exportação do JOBS_BY_PROJECT

A partir de um script SQL, é possível criar uma tabela em dataset com todas as informações da JOBS_BY_PROJECT.

```
CREATE OR REPLACE TABLE just-lore-435816-v8.billing.jobs
SELECT *
FROM region-southamerica-east1.INFORMATION_SCHEMA.JOBS_BY_PROJECT
```

### Adição de colunas

Porém, além de criar ela, devemos adicionar uma coluna de preço para cada job. Como base, usamos a [documentaçao do BigQuery](https://cloud.google.com/bigquery/pricing?hl=pt-br).

Ou seja, para cada TB gasto, R$64,00 serão cobrados. Portanto, devemos converter o total de bytes gasto em TB, divindo-o por 10^12 e, por fim, multiplicando por 64.

```
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

Como devemos manter atualizada essa tabela, uma rotina no DataForm para sua recriação seria custosa, logo, criamos usamos o MERGE, comando incremental do SQL, para adicionarmos somente as linhas que não estão nela.

```
MERGE INTO integracaohomologado.billing.jobs AS target
USING (
  SELECT creation_time,
    project_id,
    project_number,
    user_email,
    job_id,
    job_type,
    statement_type,
    start_time,
    end_time,
    total_bytes_processed,
    labels,
    total_bytes_billed,
    parent_job_id,
    (total_bytes_billed / POW(10, 12)) * 64 AS price
  FROM region-southamerica-east1.INFORMATION_SCHEMA.JOBS_BY_PROJECT AS jobs
  WHERE total_bytes_billed > 0
) AS source
ON target.job_id = source.job_id
WHEN NOT MATCHED THEN
  INSERT (creation_time,
    project_id,
    project_number,
    user_email,
    job_id,
    job_type,
    statement_type,
    start_time,
    end_time,
    total_bytes_processed,
    labels,
    total_bytes_billed,
    parent_job_id,
    price)
  VALUES (source.creation_time,
    source.project_id,
    source.project_number,
    source.user_email,
    source.job_id,
    source.job_type,
    source.statement_type,
    source.start_time,
    source.end_time,
    source.total_bytes_processed,
    source.labels,
    source.total_bytes_billed,
    source.parent_job_id,
    source.price);
```

Nesse caso, fomos obrigados a indicar as colunas a serem atualizadas, assim, decidimos em reduzir a tabela a apenas as colunas que iremos usar.