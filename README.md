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
        │
        ▼
     BRONZE
        │
        │ Ingestão e padronização técnica
        ▼
     SILVER
        │
        │ Tratamento, tipagem,
        │ deduplicação e validação
        ▼
      GOLD
        │
        │ Agregações e indicadores
        ▼
Análises de Negócio

