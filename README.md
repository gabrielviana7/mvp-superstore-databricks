# MVP Superstore — Engenharia de Dados com Databricks

MVP de Engenharia de Dados desenvolvido utilizando **Databricks**, **SQL** e arquitetura **Medallion (Bronze, Silver e Gold)**.

O projeto realiza a ingestão, tratamento, validação e análise de dados de vendas do dataset **Sample Superstore**.

---

## 🎯 Objetivo

Construir um pipeline de dados capaz de transformar dados brutos de vendas em informações estruturadas para análise de negócio.

O projeto busca analisar:

- faturamento;
- lucratividade;
- descontos;
- desempenho por categoria;
- desempenho por região;
- desempenho por subcategoria;
- subcategorias com prejuízo.

---

## 🏗️ Arquitetura

O pipeline utiliza três camadas:

```text
SampleSuperstore.csv
        |
        v
     BRONZE
        |
        | Ingestão e padronização técnica
        v
     SILVER
        |
        | Tratamento, tipagem,
        | deduplicação e validação
        v
      GOLD
        |
        | Agregações e indicadores
        v
Análises de Negócio
```

### Camada Bronze

Camada responsável pela ingestão dos dados da fonte, mantendo os registros próximos da origem e realizando os ajustes técnicos necessários para armazenamento.

**Tabela:**

`workspace.bronze.superstore_raw`

Principais atividades:

- leitura do arquivo CSV;
- ingestão dos dados;
- padronização técnica dos nomes das colunas.

### Camada Silver

Camada responsável pelo tratamento e preparação dos dados para análise.

**Tabela:**

`workspace.silver.superstore_sales`

Nesta camada são aplicados:

- padronização dos tipos de dados;
- remoção de duplicidades;
- validação de valores;
- aplicação de regras básicas de qualidade.

### Camada Gold

Camada responsável pela organização dos dados tratados em estruturas orientadas às análises de negócio.

Principais tabelas:

- `workspace.gold.vendas_categoria`
- `workspace.gold.desempenho_regional`
- `workspace.gold.desempenho_subcategoria`

---

## 🛠️ Tecnologias utilizadas

- **Databricks**
- **SQL**
- **Delta Lake**
- **Unity Catalog**
- **GitHub**

---

## 📊 Qualidade dos dados

Na camada Bronze foram identificados:

- **9.994 registros totais**
- **9.977 registros distintos**
- **17 registros duplicados em excesso**

Após o tratamento e deduplicação, a camada Silver possui:

- **9.977 registros**
- **9.977 registros distintos**

Também foram realizadas validações de valores nulos e regras de consistência.

As regras aplicadas na Silver incluem:

```text
sales > 0
quantity > 0
discount BETWEEN 0 AND 1
```

Registros com prejuízo não foram removidos, pois valores negativos de lucro podem representar situações legítimas de perda em uma venda.

---

## 📈 Principais indicadores

Após o tratamento dos dados, foram obtidos os seguintes indicadores:

| Indicador | Resultado |
|---|---:|
| Registros analisados | 9.977 |
| Faturamento total | 2.296.195,81 |
| Lucro total | 286.242,20 |
| Margem de lucro | 12,47% |
| Desconto médio | 15,63% |
| Quantidade total de produtos | 37.820 |

---

## 🔎 Análises realizadas

O projeto contempla análises de:

### Desempenho por categoria

Comparação de:

- faturamento;
- lucro;
- quantidade de vendas;
- quantidade de produtos;
- desconto médio.

### Desempenho regional

Comparação entre:

- West;
- East;
- Central;
- South.

### Desempenho por subcategoria

Análise de:

- faturamento;
- lucro;
- margem de lucro;
- desconto médio.

Também foram identificadas três subcategorias que apresentaram resultado negativo:

- Tables;
- Bookcases;
- Supplies.

---

## 📁 Estrutura do projeto

```text
mvp-superstore-databricks/
│
├── README.md
│
└── MVP_Superstore_Pipeline.py
```

O arquivo `MVP_Superstore_Pipeline.py` contém o notebook exportado do Databricks, incluindo as etapas de ingestão, tratamento, validação, criação das tabelas Gold e análises.

---

## 📚 Fonte dos dados

**Dataset:** Sample Superstore

**Arquivo:** `SampleSuperstore.csv`

O arquivo foi carregado para um Volume do Databricks e utilizado como fonte para a camada Bronze.

Caminho utilizado no Databricks:

`/Volumes/workspace/bronze/raw_files/SampleSuperstore.csv`

---

## 🚀 Fluxo do Pipeline

O fluxo completo do projeto é:

```text
Fonte CSV
   |
   v
Bronze
   |
   v
Validação da qualidade
   |
   v
Silver
   |
   |-- Deduplicação
   |-- Tipagem
   |-- Validação
   |
   v
Gold
   |
   v
Análises de Negócio
```

---

## 📋 Camadas e tabelas

| Camada | Tabela | Finalidade |
|---|---|---|
| Bronze | `workspace.bronze.superstore_raw` | Ingestão dos dados brutos |
| Silver | `workspace.silver.superstore_sales` | Tratamento e preparação dos dados |
| Gold | `workspace.gold.vendas_categoria` | Análise por categoria |
| Gold | `workspace.gold.desempenho_regional` | Análise regional |
| Gold | `workspace.gold.desempenho_subcategoria` | Análise por subcategoria |

---

## 🔬 Principais resultados

O conjunto tratado possui **9.977 registros**, com faturamento total de **2.296.195,81** e lucro total de **286.242,20**.

A margem de lucro calculada sobre o faturamento total foi de **12,47%**, enquanto o desconto médio foi de **15,63%**.

Na análise por subcategoria, foram identificadas três subcategorias com lucro negativo:

- **Tables:** -17.725,59
- **Bookcases:** -3.472,56
- **Supplies:** -1.188,99

Esses resultados são utilizados como indicadores para análise do desempenho comercial.

---

## 💻 Execução

O pipeline foi desenvolvido e executado no **Databricks**, utilizando SQL e arquitetura Bronze, Silver e Gold.

O código-fonte do notebook está disponível neste repositório em:

`MVP_Superstore_Pipeline.py`

---

## 👨‍💻 Projeto

**MVP de Engenharia de Dados — Superstore**

Projeto desenvolvido com foco em ingestão, tratamento, qualidade de dados, modelagem analítica e geração de indicadores de negócio utilizando Databricks.
