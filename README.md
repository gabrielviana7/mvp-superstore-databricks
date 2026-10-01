# MVP Superstore — Engenharia de Dados com Databricks

MVP de Engenharia de Dados desenvolvido utilizando **Databricks**, **SQL** e arquitetura **Bronze, Silver e Gold**.

O projeto implementa um pipeline de dados de ponta a ponta, desde a ingestão do arquivo bruto até a preparação de dados para análise de negócio.

---

# 1. Contexto de Negócios e Perguntas

## 1.1 Contexto

O projeto utiliza o dataset **Sample Superstore**, contendo registros de vendas de uma operação de varejo.

O objetivo é transformar os dados brutos em informações estruturadas que permitam analisar faturamento, lucratividade, descontos e desempenho comercial.

O conjunto utilizado neste projeto contém os seguintes atributos:

- Ship Mode
- Segment
- Country
- City
- State
- Postal Code
- Region
- Category
- Sub-Category
- Sales
- Quantity
- Discount
- Profit

Após a padronização técnica realizada na camada Bronze, os nomes das colunas foram convertidos para o padrão utilizado no pipeline.

---

## 1.2 Perguntas de negócio

O pipeline foi construído para responder às seguintes perguntas:

1. Quais categorias apresentam maior faturamento e maior lucro?

2. Quais regiões apresentam maior faturamento e maior lucro?

3. Quais subcategorias apresentam prejuízo?

4. Quais subcategorias apresentam as maiores margens de lucro?

5. Qual é o faturamento total, lucro total e margem de lucro do conjunto analisado?

6. Qual é o desconto médio aplicado nas vendas e como esse indicador se comporta entre categorias, regiões e subcategorias?

Essas perguntas orientaram as etapas de modelagem, transformação e análise do pipeline.

---

## 1.3 Fonte dos dados

**Dataset:** Sample Superstore

**Arquivo:** `SampleSuperstore.csv`

**Fonte:** Kaggle

O arquivo foi baixado e posteriormente carregado para um Volume do Databricks.

**Caminho utilizado:**

`/Volumes/workspace/bronze/raw_files/SampleSuperstore.csv`

### Licença

A licença de uso deve ser considerada conforme a informação disponibilizada na página original do dataset no Kaggle.

**Fonte original:** Kaggle — Sample Superstore

---

# 2. Carga dos Dados

A coleta utilizada neste MVP foi realizada por meio de um arquivo CSV disponibilizado pelo Kaggle.

O arquivo `SampleSuperstore.csv` foi baixado e carregado para um **Volume do Databricks**, permitindo que o pipeline realizasse a leitura diretamente no ambiente de nuvem.

A ingestão foi realizada utilizando a função `read_files()` do Databricks.

O arquivo foi utilizado como fonte para a criação da camada Bronze:

`workspace.bronze.superstore_raw`

O código responsável pela ingestão está disponível no arquivo:

`MVP_Superstore_Pipeline.py`

---

# 3. Modelagem e Catálogo de Dados

## 3.1 Arquitetura

O projeto utiliza uma organização em três camadas:

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

---

## 3.2 Camada Bronze

A camada Bronze representa a entrada dos dados no ambiente Databricks.

**Tabela:**

`workspace.bronze.superstore_raw`

Principais atividades:

- leitura do arquivo CSV;
- ingestão dos registros;
- padronização técnica dos nomes das colunas.

A Bronze apresentou inicialmente:

- 9.994 registros;
- 9.977 registros distintos.

---

## 3.3 Camada Silver

A camada Silver contém os dados tratados e preparados para análise.

**Tabela:**

`workspace.silver.superstore_sales`

Principais transformações:

- padronização dos tipos de dados;
- conversão de campos numéricos;
- remoção de duplicidades;
- validação dos valores;
- aplicação de regras básicas de qualidade.

Regras utilizadas:

```text
sales > 0
quantity > 0
discount BETWEEN 0 AND 1
```

Após o tratamento, a Silver possui:

- 9.977 registros;
- 9.977 registros distintos.

---

## 3.4 Camada Gold

A camada Gold organiza os dados para responder às perguntas de negócio.

### Vendas por categoria

`workspace.gold.vendas_categoria`

Permite analisar:

- faturamento;
- lucro;
- quantidade de vendas;
- quantidade de produtos;
- desconto médio.

### Desempenho regional

`workspace.gold.desempenho_regional`

Permite analisar o desempenho por região.

### Desempenho por subcategoria

`workspace.gold.desempenho_subcategoria`

Permite analisar:

- faturamento;
- lucro;
- margem de lucro;
- desconto médio.

---

## 3.5 Catálogo de Dados

### `workspace.silver.superstore_sales`

| Campo | Tipo | Descrição | Regra / Domínio |
|---|---|---|---|
| `ship_mode` | STRING | Modalidade de envio | Categorias de modalidade de envio |
| `segment` | STRING | Segmento do cliente | Consumer, Corporate, Home Office |
| `country` | STRING | País | País de origem do registro |
| `city` | STRING | Cidade | Cidade da venda |
| `state` | STRING | Estado | Estado da venda |
| `postal_code` | STRING | Código postal | Código postal |
| `region` | STRING | Região | West, East, Central, South |
| `category` | STRING | Categoria do produto | Technology, Furniture, Office Supplies |
| `sub_category` | STRING | Subcategoria do produto | Subcategorias existentes no dataset |
| `sales` | DECIMAL(18,2) | Valor da venda | Maior que zero |
| `quantity` | INT | Quantidade de produtos | Maior que zero |
| `discount` | DECIMAL(5,2) | Desconto aplicado | Entre 0 e 1 |
| `profit` | DECIMAL(18,2) | Lucro ou prejuízo da venda | Pode ser positivo ou negativo |

### Linhagem

```text
SampleSuperstore.csv
        |
        v
workspace.bronze.superstore_raw
        |
        | deduplicação
        | tipagem
        | validação
        v
workspace.silver.superstore_sales
        |
        | agregações
        v
workspace.gold.*
```

---

# 4. Pipeline de Dados

O pipeline foi desenvolvido em um único notebook Databricks:

`MVP_Superstore_Pipeline`

O notebook contém as etapas de:

1. ingestão da fonte;
2. criação da Bronze;
3. validação da Bronze;
4. criação da Silver;
5. validação da Silver;
6. criação das tabelas Gold;
7. análises de negócio;
8. consolidação dos indicadores.

O código-fonte exportado do notebook está disponível no GitHub em:

`MVP_Superstore_Pipeline.py`

---

# 5. Qualidade de Dados

Foram realizadas verificações de qualidade considerando completude, unicidade e consistência dos dados.

## 5.1 Unicidade

Na Bronze foram encontrados:

- 9.994 registros totais;
- 9.977 registros distintos.

Isso representa 17 registros duplicados em excesso.

Os registros duplicados foram removidos durante a criação da Silver.

Após o tratamento:

- 9.977 registros totais;
- 9.977 registros distintos.

---

## 5.2 Completude

Foram realizadas verificações de valores nulos nos atributos da Bronze e da Silver.

Não foram identificados valores nulos nos campos analisados.

---

## 5.3 Consistência

Foram verificadas as seguintes regras:

```text
sales > 0
quantity > 0
discount BETWEEN 0 AND 1
```

Não foram identificados registros fora dessas regras.

Valores negativos de `profit` foram mantidos, pois representam vendas que apresentaram prejuízo e não necessariamente erros de dados.

---

# 6. Análise de Dados

## 6.1 Indicadores gerais

| Indicador | Resultado |
|---|---:|
| Registros analisados | 9.977 |
| Faturamento total | 2.296.195,81 |
| Lucro total | 286.242,20 |
| Margem de lucro | 12,47% |
| Desconto médio | 15,63% |
| Quantidade total de produtos | 37.820 |

---

## 6.2 Categorias

As três categorias analisadas foram:

- Technology
- Furniture
- Office Supplies

A análise permite comparar faturamento, lucro, quantidade de vendas, quantidade de produtos e desconto médio entre as categorias.

---

## 6.3 Regiões

As regiões analisadas foram:

- West
- East
- Central
- South

A análise regional permite comparar faturamento, lucro, quantidade de vendas e desconto médio.

---

## 6.4 Subcategorias com prejuízo

Foram identificadas três subcategorias com lucro negativo:

| Subcategoria | Faturamento | Lucro |
|---|---:|---:|
| Tables | 206.965,68 | -17.725,59 |
| Bookcases | 114.880,05 | -3.472,56 |
| Supplies | 46.673,52 | -1.188,99 |

Essas subcategorias foram identificadas a partir da análise da tabela `workspace.gold.desempenho_subcategoria`.

---

## 6.5 Margem de lucro

A margem de lucro foi calculada pela relação entre lucro e faturamento:

```text
Margem = (Lucro / Faturamento) × 100
```

A análise permitiu identificar subcategorias com margens positivas e negativas.

As três subcategorias com resultado negativo foram:

- Tables: -8,56%
- Bookcases: -3,02%
- Supplies: -2,55%

---

# 7. Conclusão

O MVP conseguiu implementar um pipeline de dados de ponta a ponta utilizando Databricks e a arquitetura Bronze, Silver e Gold.

O fluxo parte de um arquivo CSV, realiza a ingestão na camada Bronze, aplica tratamento e validações na Silver e organiza os dados em tabelas Gold destinadas às análises de negócio.

As análises realizadas permitem responder às perguntas definidas no objetivo, principalmente em relação a faturamento, lucratividade, desempenho regional, desempenho por categoria e subcategorias com prejuízo.

---

# 8. Evidências da Execução

As evidências visuais do projeto devem ser apresentadas nesta seção, incluindo screenshots do ambiente Databricks e dos resultados das consultas.

### Evidência 1 — Arquivo fonte no Volume

*Inserir screenshot do arquivo `SampleSuperstore.csv` no Volume do Databricks.*

### Evidência 2 — Camada Bronze

*Inserir screenshot da tabela `workspace.bronze.superstore_raw` e da validação de registros.*

### Evidência 3 — Camada Silver

*Inserir screenshot da tabela `workspace.silver.superstore_sales` e da validação de registros.*

### Evidência 4 — Camada Gold

*Inserir screenshot das tabelas Gold criadas no Databricks.*

### Evidência 5 — Qualidade dos dados

*Inserir screenshot das consultas de qualidade e seus resultados.*

### Evidência 6 — Análises de negócio

*Inserir screenshot dos resultados das consultas de análise e dos principais indicadores.*

---

# 9. Autoavaliação

## Atingimento dos objetivos

O objetivo principal do MVP foi atingido com a construção de um pipeline funcional de dados utilizando Databricks e arquitetura Bronze, Silver e Gold.

Foi possível realizar a ingestão dos dados, tratar problemas de qualidade, estruturar as camadas analíticas e executar consultas para responder às perguntas de negócio definidas.

## Dificuldades encontradas

As principais dificuldades estiveram relacionadas à configuração inicial do ambiente Databricks, organização das camadas no Unity Catalog, ingestão do arquivo CSV e tratamento de duplicidades e tipos de dados.

Também foi necessário organizar o notebook para manter o código das etapas do pipeline documentado e reproduzível.

## Trabalhos futuros

Como evolução do projeto, poderiam ser implementados:

- atualização automatizada da fonte de dados;
- monitoramento de qualidade;
- criação de dashboards;
- análises temporais caso uma fonte com informações de data seja incorporada;
- criação de métricas adicionais de desempenho;
- automação da execução do pipeline.

---

# 10. Tecnologias

- Databricks
- SQL
- Delta Lake
- Unity Catalog
- GitHub

---

# 11. Estrutura do Repositório

```text
mvp-superstore-databricks/
│
├── README.md
│
└── MVP_Superstore_Pipeline.py
```

O arquivo `MVP_Superstore_Pipeline.py` contém o notebook exportado do Databricks com o código utilizado na construção do pipeline.

---

# 12. Fonte

Dataset utilizado:

**Sample Superstore — Kaggle**
https://www.kaggle.com/datasets/xubao666/superstore?utm_source=chatgpt.com

Arquivo:

`SampleSuperstore.csv`

O dataset foi utilizado exclusivamente como fonte de dados para o desenvolvimento deste MVP.
