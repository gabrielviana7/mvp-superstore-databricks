# Databricks notebook source
# MAGIC %md
# MAGIC # MVP Superstore — Pipeline de Dados
# MAGIC
# MAGIC ## Objetivo
# MAGIC
# MAGIC Construir um pipeline de dados utilizando a arquitetura **Bronze, Silver e Gold** para ingestão, tratamento, validação e análise dos dados de vendas do dataset **Sample Superstore**.
# MAGIC
# MAGIC O projeto tem como objetivo analisar:
# MAGIC
# MAGIC - faturamento;
# MAGIC - lucratividade;
# MAGIC - descontos;
# MAGIC - desempenho por categoria;
# MAGIC - desempenho por região;
# MAGIC - desempenho por subcategoria;
# MAGIC - subcategorias com prejuízo.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Fonte dos dados
# MAGIC
# MAGIC **Dataset:** Sample Superstore  
# MAGIC **Arquivo:** `SampleSuperstore.csv`
# MAGIC
# MAGIC O arquivo foi disponibilizado em um Volume do Databricks:
# MAGIC
# MAGIC `/Volumes/workspace/bronze/raw_files/SampleSuperstore.csv`
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Arquitetura do Pipeline
# MAGIC
# MAGIC ```text
# MAGIC SampleSuperstore.csv
# MAGIC         │
# MAGIC         ▼
# MAGIC      BRONZE
# MAGIC         │
# MAGIC         │ Ingestão e padronização técnica
# MAGIC         ▼
# MAGIC      SILVER
# MAGIC         │
# MAGIC         │ Tratamento, tipagem,
# MAGIC         │ deduplicação e validação
# MAGIC         ▼
# MAGIC       GOLD
# MAGIC         │
# MAGIC         │ Agregações e indicadores
# MAGIC         ▼
# MAGIC Análises de Negócio
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Camada Bronze
# MAGIC
# MAGIC Responsável pela ingestão dos dados da fonte, mantendo os registros próximos da origem e realizando os ajustes técnicos necessários para armazenamento.
# MAGIC
# MAGIC Tabela:
# MAGIC
# MAGIC workspace.bronze.superstore_raw
# MAGIC
# MAGIC Camada Silver
# MAGIC
# MAGIC Responsável pelo tratamento e preparação dos dados para análise.
# MAGIC
# MAGIC Nesta camada são aplicados:
# MAGIC
# MAGIC padronização dos tipos de dados;
# MAGIC remoção de duplicidades;
# MAGIC validação de valores;
# MAGIC aplicação de regras básicas de qualidade.
# MAGIC
# MAGIC Tabela:
# MAGIC
# MAGIC workspace.silver.superstore_sales
# MAGIC
# MAGIC Camada Gold
# MAGIC
# MAGIC Responsável pela organização dos dados tratados em estruturas orientadas às análises de negócio.
# MAGIC
# MAGIC Principais tabelas:
# MAGIC
# MAGIC workspace.gold.vendas_categoria
# MAGIC workspace.gold.desempenho_regional
# MAGIC workspace.gold.desempenho_subcategoria
# MAGIC Tecnologias utilizadas
# MAGIC Databricks
# MAGIC SQL
# MAGIC Delta Lake
# MAGIC Unity Catalog
# MAGIC GitHub
# MAGIC Fluxo de execução
# MAGIC Leitura do arquivo SampleSuperstore.csv
# MAGIC Criação da camada Bronze
# MAGIC Validação da qualidade dos dados da Bronze
# MAGIC Criação da camada Silver
# MAGIC Tratamento e deduplicação dos registros
# MAGIC Validação da qualidade da Silver
# MAGIC Criação das tabelas da camada Gold
# MAGIC Análises de negócio
# MAGIC Consolidação dos principais indicadores
# MAGIC Documentação dos resultados
# MAGIC Estrutura do Notebook
# MAGIC
# MAGIC O notebook está organizado seguindo as etapas do pipeline:
# MAGIC
# MAGIC Bronze → Silver → Gold → Análises de Negócio
# MAGIC
# MAGIC Cada etapa contém as consultas SQL utilizadas para construção, tratamento, validação e análise dos dados.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.bronze.superstore_raw
# MAGIC AS
# MAGIC SELECT
# MAGIC     `Ship Mode` AS ship_mode,
# MAGIC     Segment AS segment,
# MAGIC     Country AS country,
# MAGIC     City AS city,
# MAGIC     State AS state,
# MAGIC     `Postal Code` AS postal_code,
# MAGIC     Region AS region,
# MAGIC     Category AS category,
# MAGIC     `Sub-Category` AS sub_category,
# MAGIC     Sales AS sales,
# MAGIC     Quantity AS quantity,
# MAGIC     Discount AS discount,
# MAGIC     Profit AS profit
# MAGIC FROM read_files(
# MAGIC     '/Volumes/workspace/bronze/raw_files/SampleSuperstore.csv',
# MAGIC     format => 'csv',
# MAGIC     header => true,
# MAGIC     inferSchema => true
# MAGIC );

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1.1. Validação da qualidade da Bronze
# MAGIC
# MAGIC Após a ingestão, são realizadas verificações para identificar:
# MAGIC
# MAGIC - quantidade total de registros;
# MAGIC - registros distintos;
# MAGIC - duplicidades;
# MAGIC - valores nulos;
# MAGIC - valores fora dos limites esperados.
# MAGIC
# MAGIC A análise inicial identificou 9.994 registros na Bronze e 9.977 registros distintos.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_registros,
# MAGIC     COUNT(DISTINCT *) AS registros_distintos
# MAGIC FROM workspace.bronze.superstore_raw;

# COMMAND ----------

# MAGIC %md
# MAGIC # 2. Camada Silver — Tratamento e Padronização
# MAGIC
# MAGIC A camada Silver transforma os dados da Bronze em uma estrutura adequada para análises.
# MAGIC
# MAGIC Nesta etapa são aplicados:
# MAGIC
# MAGIC - padronização dos tipos de dados;
# MAGIC - conversão de campos numéricos;
# MAGIC - remoção de registros duplicados;
# MAGIC - validação de valores de negócio;
# MAGIC - exclusão de registros com valores inválidos.
# MAGIC
# MAGIC Regras aplicadas:
# MAGIC
# MAGIC - `sales > 0`
# MAGIC - `quantity > 0`
# MAGIC - `discount BETWEEN 0 AND 1`
# MAGIC
# MAGIC Tabela de destino:
# MAGIC
# MAGIC `workspace.silver.superstore_sales`

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE workspace.silver.superstore_sales
# MAGIC AS
# MAGIC SELECT DISTINCT
# MAGIC     CAST(ship_mode AS STRING) AS ship_mode,
# MAGIC     CAST(segment AS STRING) AS segment,
# MAGIC     CAST(country AS STRING) AS country,
# MAGIC     CAST(city AS STRING) AS city,
# MAGIC     CAST(state AS STRING) AS state,
# MAGIC     CAST(postal_code AS STRING) AS postal_code,
# MAGIC     CAST(region AS STRING) AS region,
# MAGIC     CAST(category AS STRING) AS category,
# MAGIC     CAST(sub_category AS STRING) AS sub_category,
# MAGIC     CAST(sales AS DECIMAL(18,2)) AS sales,
# MAGIC     CAST(quantity AS INT) AS quantity,
# MAGIC     CAST(discount AS DECIMAL(5,2)) AS discount,
# MAGIC     CAST(profit AS DECIMAL(18,2)) AS profit
# MAGIC FROM workspace.bronze.superstore_raw
# MAGIC WHERE sales > 0
# MAGIC   AND quantity > 0
# MAGIC   AND discount BETWEEN 0 AND 1;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2.1. Validação da Silver
# MAGIC
# MAGIC Após o tratamento, a Silver é novamente validada para confirmar a quantidade de registros e a ausência de duplicidades.
# MAGIC
# MAGIC Resultado esperado:
# MAGIC
# MAGIC - 9.977 registros;
# MAGIC - 9.977 registros distintos.

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 05. QUALIDADE DA SILVER
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_registros,
# MAGIC     COUNT(DISTINCT *) AS registros_distintos
# MAGIC FROM workspace.silver.superstore_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- Verificação de valores nulos na Silver
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT_IF(ship_mode IS NULL) AS nulos_ship_mode,
# MAGIC     COUNT_IF(segment IS NULL) AS nulos_segment,
# MAGIC     COUNT_IF(country IS NULL) AS nulos_country,
# MAGIC     COUNT_IF(city IS NULL) AS nulos_city,
# MAGIC     COUNT_IF(state IS NULL) AS nulos_state,
# MAGIC     COUNT_IF(postal_code IS NULL) AS nulos_postal_code,
# MAGIC     COUNT_IF(region IS NULL) AS nulos_region,
# MAGIC     COUNT_IF(category IS NULL) AS nulos_category,
# MAGIC     COUNT_IF(sub_category IS NULL) AS nulos_sub_category,
# MAGIC     COUNT_IF(sales IS NULL) AS nulos_sales,
# MAGIC     COUNT_IF(quantity IS NULL) AS nulos_quantity,
# MAGIC     COUNT_IF(discount IS NULL) AS nulos_discount,
# MAGIC     COUNT_IF(profit IS NULL) AS nulos_profit
# MAGIC FROM workspace.silver.superstore_sales;

# COMMAND ----------

# MAGIC %md
# MAGIC # 3. Camada Gold — Dados para Análise
# MAGIC
# MAGIC A camada Gold consolida os dados tratados da Silver em estruturas orientadas à análise de negócio.
# MAGIC
# MAGIC Foram criadas três visões principais:
# MAGIC
# MAGIC ### Vendas por categoria
# MAGIC
# MAGIC `workspace.gold.vendas_categoria`
# MAGIC
# MAGIC Permite analisar faturamento, lucro, quantidade de vendas e desconto médio por categoria.
# MAGIC
# MAGIC ### Desempenho regional
# MAGIC
# MAGIC `workspace.gold.desempenho_regional`
# MAGIC
# MAGIC Permite comparar o desempenho das regiões.
# MAGIC
# MAGIC ### Desempenho por subcategoria
# MAGIC
# MAGIC `workspace.gold.desempenho_subcategoria`
# MAGIC
# MAGIC Permite analisar faturamento, lucro e desconto médio por subcategoria.

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 06. GOLD - VENDAS POR CATEGORIA
# MAGIC -- ============================================================
# MAGIC
# MAGIC CREATE OR REPLACE TABLE workspace.gold.vendas_categoria AS
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     COUNT(*) AS quantidade_vendas,
# MAGIC     SUM(quantity) AS quantidade_produtos,
# MAGIC     ROUND(SUM(sales), 2) AS faturamento,
# MAGIC     ROUND(SUM(profit), 2) AS lucro,
# MAGIC     ROUND(AVG(discount), 4) AS desconto_medio
# MAGIC FROM workspace.silver.superstore_sales
# MAGIC GROUP BY category
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM workspace.gold.vendas_categoria
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 06. GOLD - DESEMPENHO REGIONAL
# MAGIC -- ============================================================
# MAGIC
# MAGIC CREATE OR REPLACE TABLE workspace.gold.desempenho_regional AS
# MAGIC
# MAGIC SELECT
# MAGIC     region,
# MAGIC     COUNT(*) AS quantidade_vendas,
# MAGIC     SUM(quantity) AS quantidade_produtos,
# MAGIC     ROUND(SUM(sales), 2) AS faturamento,
# MAGIC     ROUND(SUM(profit), 2) AS lucro,
# MAGIC     ROUND(AVG(discount), 4) AS desconto_medio
# MAGIC FROM workspace.silver.superstore_sales
# MAGIC GROUP BY region
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM workspace.gold.desempenho_regional
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 06. GOLD - DESEMPENHO POR SUBCATEGORIA
# MAGIC -- ============================================================
# MAGIC
# MAGIC CREATE OR REPLACE TABLE workspace.gold.desempenho_subcategoria AS
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     sub_category,
# MAGIC     COUNT(*) AS quantidade_vendas,
# MAGIC     SUM(quantity) AS quantidade_produtos,
# MAGIC     ROUND(SUM(sales), 2) AS faturamento,
# MAGIC     ROUND(SUM(profit), 2) AS lucro,
# MAGIC     ROUND(AVG(discount), 4) AS desconto_medio
# MAGIC FROM workspace.silver.superstore_sales
# MAGIC GROUP BY
# MAGIC     category,
# MAGIC     sub_category
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT *
# MAGIC FROM workspace.gold.desempenho_subcategoria
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC # 4. Análises de Negócio
# MAGIC
# MAGIC As consultas desta seção utilizam as tabelas da camada Gold para responder perguntas relacionadas ao desempenho das vendas e à lucratividade.
# MAGIC
# MAGIC São analisados:
# MAGIC
# MAGIC - desempenho das categorias;
# MAGIC - desempenho regional;
# MAGIC - subcategorias com prejuízo;
# MAGIC - maiores faturamentos;
# MAGIC - margem de lucro por subcategoria.

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 07. ANÁLISES DE NEGÓCIO
# MAGIC -- Pergunta 1: desempenho por categoria
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     faturamento,
# MAGIC     lucro,
# MAGIC     desconto_medio,
# MAGIC     quantidade_vendas
# MAGIC FROM workspace.gold.vendas_categoria
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- Pergunta 2: desempenho regional
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     region,
# MAGIC     faturamento,
# MAGIC     lucro,
# MAGIC     desconto_medio,
# MAGIC     quantidade_vendas
# MAGIC FROM workspace.gold.desempenho_regional
# MAGIC ORDER BY faturamento DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- Pergunta 3: subcategorias com prejuízo
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     sub_category,
# MAGIC     faturamento,
# MAGIC     lucro,
# MAGIC     desconto_medio
# MAGIC FROM workspace.gold.desempenho_subcategoria
# MAGIC WHERE lucro < 0
# MAGIC ORDER BY lucro ASC;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- Pergunta 4: maiores faturamentos por subcategoria
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     sub_category,
# MAGIC     faturamento,
# MAGIC     lucro,
# MAGIC     desconto_medio
# MAGIC FROM workspace.gold.desempenho_subcategoria
# MAGIC ORDER BY faturamento DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- Pergunta 5: margem de lucro por subcategoria
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     category,
# MAGIC     sub_category,
# MAGIC     faturamento,
# MAGIC     lucro,
# MAGIC     ROUND(
# MAGIC         (lucro / NULLIF(faturamento, 0)) * 100,
# MAGIC         2
# MAGIC     ) AS margem_lucro_percentual,
# MAGIC     desconto_medio
# MAGIC FROM workspace.gold.desempenho_subcategoria
# MAGIC ORDER BY margem_lucro_percentual ASC;

# COMMAND ----------

# MAGIC %md
# MAGIC # 5. Indicadores Gerais
# MAGIC
# MAGIC Esta seção consolida os principais indicadores do dataset tratado na camada Silver.
# MAGIC
# MAGIC Os indicadores considerados são:
# MAGIC
# MAGIC - total de registros;
# MAGIC - faturamento total;
# MAGIC - lucro total;
# MAGIC - margem de lucro;
# MAGIC - desconto médio;
# MAGIC - quantidade total de produtos.

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 08. KPIs GERAIS DO NEGÓCIO
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_registros,
# MAGIC     ROUND(SUM(sales), 2) AS faturamento_total,
# MAGIC     ROUND(SUM(profit), 2) AS lucro_total,
# MAGIC     ROUND(
# MAGIC         (SUM(profit) / NULLIF(SUM(sales), 0)) * 100,
# MAGIC         2
# MAGIC     ) AS margem_lucro_percentual,
# MAGIC     ROUND(AVG(discount) * 100, 2) AS desconto_medio_percentual,
# MAGIC     SUM(quantity) AS quantidade_total_produtos
# MAGIC FROM workspace.silver.superstore_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- ============================================================
# MAGIC -- 08. RESUMO DE RENTABILIDADE
# MAGIC -- ============================================================
# MAGIC
# MAGIC SELECT
# MAGIC     COUNT_IF(lucro < 0) AS subcategorias_com_prejuizo,
# MAGIC     COUNT(*) AS total_subcategorias,
# MAGIC     ROUND(SUM(lucro), 2) AS lucro_total,
# MAGIC     ROUND(SUM(faturamento), 2) AS faturamento_total
# MAGIC FROM workspace.gold.desempenho_subcategoria;

# COMMAND ----------

# MAGIC %md
# MAGIC # 08. Conclusões e Insights
# MAGIC
# MAGIC ## Visão geral
# MAGIC
# MAGIC O pipeline processou o dataset Sample Superstore utilizando uma arquitetura
# MAGIC Bronze, Silver e Gold.
# MAGIC
# MAGIC Após a ingestão e as validações de qualidade, foram analisados 9.977 registros.
# MAGIC
# MAGIC ## KPIs
# MAGIC
# MAGIC - Faturamento total: 2.296.195,81
# MAGIC - Lucro total: 286.242,20
# MAGIC - Margem de lucro: 12,47%
# MAGIC - Desconto médio: 15,63%
# MAGIC - Quantidade total de produtos: 37.820
# MAGIC
# MAGIC ## Principais insights
# MAGIC
# MAGIC ### Categorias
# MAGIC
# MAGIC Technology apresentou o maior faturamento e também o maior lucro agregado
# MAGIC entre as categorias analisadas.
# MAGIC
# MAGIC ### Regiões
# MAGIC
# MAGIC A região West apresentou o maior faturamento e o maior lucro agregado.
# MAGIC
# MAGIC ### Rentabilidade
# MAGIC
# MAGIC Foram identificadas 3 subcategorias com lucro negativo entre as 17 analisadas:
# MAGIC
# MAGIC - Tables
# MAGIC - Bookcases
# MAGIC - Supplies
# MAGIC
# MAGIC Tables apresentou faturamento superior a 200 mil, mas margem de lucro negativa
# MAGIC de -8,56%, demonstrando que volume de faturamento não representa
# MAGIC necessariamente rentabilidade positiva.
# MAGIC
# MAGIC ## Qualidade dos dados
# MAGIC
# MAGIC A análise da camada Bronze identificou:
# MAGIC
# MAGIC - 9.994 registros;
# MAGIC - 17 registros duplicados;
# MAGIC - nenhum valor nulo;
# MAGIC - nenhuma venda com valor inválido;
# MAGIC - nenhuma quantidade inválida;
# MAGIC - nenhum desconto fora do intervalo esperado.
# MAGIC
# MAGIC As duplicidades foram removidas na camada Silver, resultando em 9.977 registros.
# MAGIC
# MAGIC ## Limitações
# MAGIC
# MAGIC A base utilizada não possui identificador de pedido ou cliente e não possui
# MAGIC uma coluna de data na versão utilizada. Portanto, não foram realizadas análises
# MAGIC de evolução temporal, retenção de clientes ou frequência de compra.
# MAGIC
# MAGIC Os resultados representam relações observadas nos dados e não permitem
# MAGIC estabelecer relações de causalidade.

# COMMAND ----------

# MAGIC %md
# MAGIC # 09. Catálogo de Dados
# MAGIC
# MAGIC ## Camada Bronze
# MAGIC
# MAGIC Tabela: `workspace.bronze.superstore_raw`
# MAGIC
# MAGIC | Campo | Tipo | Descrição |
# MAGIC |---|---|---|
# MAGIC | ship_mode | STRING | Modalidade de envio |
# MAGIC | segment | STRING | Segmento do cliente |
# MAGIC | country | STRING | País |
# MAGIC | city | STRING | Cidade |
# MAGIC | state | STRING | Estado |
# MAGIC | postal_code | STRING | Código postal |
# MAGIC | region | STRING | Região |
# MAGIC | category | STRING | Categoria do produto |
# MAGIC | sub_category | STRING | Subcategoria do produto |
# MAGIC | sales | DOUBLE/DECIMAL | Valor da venda |
# MAGIC | quantity | INT | Quantidade de produtos |
# MAGIC | discount | DOUBLE/DECIMAL | Percentual de desconto |
# MAGIC | profit | DOUBLE/DECIMAL | Lucro ou prejuízo da venda |
# MAGIC
# MAGIC ## Camada Silver
# MAGIC
# MAGIC Tabela: `workspace.silver.superstore_sales`
# MAGIC
# MAGIC A Silver contém os mesmos atributos da Bronze, porém com:
# MAGIC
# MAGIC - nomes de colunas padronizados;
# MAGIC - tipos de dados definidos;
# MAGIC - registros duplicados removidos;
# MAGIC - validações de vendas, quantidade e desconto aplicadas.
# MAGIC
# MAGIC Quantidade de registros: **9.977**.
# MAGIC
# MAGIC ## Camada Gold
# MAGIC
# MAGIC ### `workspace.gold.vendas_categoria`
# MAGIC
# MAGIC Agrega os dados por categoria.
# MAGIC
# MAGIC Principais métricas:
# MAGIC
# MAGIC - quantidade de vendas;
# MAGIC - quantidade de produtos;
# MAGIC - faturamento;
# MAGIC - lucro;
# MAGIC - desconto médio.
# MAGIC
# MAGIC ### `workspace.gold.desempenho_regional`
# MAGIC
# MAGIC Agrega os dados por região.
# MAGIC
# MAGIC Principais métricas:
# MAGIC
# MAGIC - quantidade de vendas;
# MAGIC - quantidade de produtos;
# MAGIC - faturamento;
# MAGIC - lucro;
# MAGIC - desconto médio.
# MAGIC
# MAGIC ### `workspace.gold.desempenho_subcategoria`
# MAGIC
# MAGIC Agrega os dados por categoria e subcategoria.
# MAGIC
# MAGIC Principais métricas:
# MAGIC
# MAGIC - quantidade de vendas;
# MAGIC - quantidade de produtos;
# MAGIC - faturamento;
# MAGIC - lucro;
# MAGIC - desconto médio.
# MAGIC
# MAGIC A partir dessa tabela também foi calculada a margem de lucro percentual nas análises.

# COMMAND ----------

# MAGIC %md
# MAGIC # 10. Arquitetura do Pipeline
# MAGIC
# MAGIC O projeto utiliza uma arquitetura de camadas Bronze, Silver e Gold.
# MAGIC
# MAGIC ```text
# MAGIC SampleSuperstore.csv
# MAGIC         |
# MAGIC         v
# MAGIC +-------------------+
# MAGIC |       BRONZE      |
# MAGIC | Dados ingeridos   |
# MAGIC | 9.994 registros   |
# MAGIC +---------+---------+
# MAGIC           |
# MAGIC           | Deduplicação
# MAGIC           | Padronização
# MAGIC           | Validação
# MAGIC           v
# MAGIC +-------------------+
# MAGIC |       SILVER      |
# MAGIC | Dados tratados    |
# MAGIC | 9.977 registros   |
# MAGIC +---------+---------+
# MAGIC           |
# MAGIC           | Agregações
# MAGIC           | Métricas
# MAGIC           v
# MAGIC +-------------------+
# MAGIC |        GOLD       |
# MAGIC +-------------------+
# MAGIC | vendas_categoria  |
# MAGIC | desempenho_regional|
# MAGIC | desempenho_subcategoria |
# MAGIC +---------+---------+
# MAGIC           |
# MAGIC           v
# MAGIC    Análises de negócio