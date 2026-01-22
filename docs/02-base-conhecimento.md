# Base de Conhecimento

## Dados Utilizados

O projeto utiliza duas fontes de dados complementares: dados mockados internos para simulação e datasets públicos do Hugging Face como base de referência analítica.

**1️⃣ Dados Mockados do Projeto (data/raw)**

Utilizados para simular investidores fictícios, comportamentos financeiros e cenários controlados durante testes e demonstrações do agente.

| Arquivo                                                    | Formato        | Utilização no Agente                                                                               |
| ---------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------- |
| `perfil_investidor.json`                                   | json           | Define perfis fictícios de investidores para simulação de comportamento financeiro                 |
| `transacoes.csv` e `movimentacoes.csv`                     | csv            | Simula histórico de transações e movimentações financeiras para análise de padrões e alertas       |

---

**2️⃣ Datasets do Hugging Face (Referência)**

Utilizados como base estatística e comportamental, apoiando a detecção de risco, fraude e inadimplência.

| Arquivo                                                            | Formato        | Utilização no Agente                                                        |
| ------------------------------------------------------------------ | -------------- | --------------------------------------------------------------------------- |
| `credit_fraud_detection.parquet` e `financial_fraud_detection.csv` | parquet / csv  | Analisa padrões de possíveis ações fraudulentas, apoiando a camada de risco |
| `credit_risk.csv`                                                  | csv            | Avalia risco de crédito, inferindo probabilidade de inadimplência           |
| `personal_finance_json.jsonl` e `personal_finance.parquet`         | json / parquet | Identifica hábitos de consumo, relação gasto vs renda e perfil financeiro   |


> [!TIP]
> **Caso deseje um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim. Os dados mockados foram expandidos e enriquecidos com datasets públicos de fraude, risco de crédito e finanças pessoais, permitindo maior variedade de cenários, padrões comportamentais realistas e melhor capacidade do agente em detectar riscos, inconsistências e situações suspeitas.
Todos os dados estão em padrão extrangeiro então a inteligência artifical irá ter que entender e adaptar para o padrão do usuário.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades, injetar os dados diretamente no prompt (Ctrl + c, Ctrl + v) ou carregar os arquivos via código, como no exemplo abaixo:

**Nota:** Crie um arquivo load_hf_datasets.py, dentro da pasta src e insira o código nele para cria uma classe Dataloader para baixar dados direto do hugging face sem a necessidade de ter os arquivos localmente.

```python
import pandas as pd

def load_credit_fraud_detection():
    splits = {
        "train": "data/train-00000-of-00001.parquet"
    }
    return pd.read_parquet(
        "hf://datasets/rohan-chandrashekar/credit_fraud_detection/" + splits["train"]
    )

def load_credit_risk():
    return pd.read_csv(
        "hf://datasets/bongpheng/credit_risk_ds_100k/credit_risk_applicants_100k.csv"
    )

def load_personal_finance_parquet():
    splits = {
        "train": "data/train-00000-of-00001-0358029db0db7cde.parquet"
    }
    return pd.read_parquet(
        "hf://datasets/danielv835/personal_finance_v0.2/" + splits["train"]
    )

def load_personal_finance_json():
    return pd.read_json(
        "hf://datasets/Akhil-Theerthala/PersonalFinance_v2/finance_cotr.jsonl",
        lines=True
    )

def load_financial_fraud_detection():
    return pd.read_csv(
        "hf://datasets/rohan-chandrashekar/Financial_Fraud_Detection/New_Dataset.csv"
    )

```

```python
# Exemplo de como usar no projeto (Dentro o arquivo app.py)

# Basic Libs
import pandas as pd

# Modules
from src.ingestion.load_hf_datasets import (
    load_credit_fraud_detection,
    load_credit_risk,
    load_personal_finance_parquet,
    load_personal_finance_json,
    load_financial_fraud_detection
)

# ============  CARREGAR DADOS ============ #
df_credit_fraud_detection_parquet = load_credit_fraud_detection()
df_credit_risk_csv = load_credit_risk()
df_personal_finance_parquet = load_personal_finance_parquet()
df_personal_finance_json = load_personal_finance_json()
df_financial_fraud_detection_csv = load_financial_fraud_detection()

```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

```text
Perfil do Investidor

Datasets:

perfil_investidor.json

Uso no prompt:
Os dados são analisados para identificar características gerais do investidor e gerar indicadores como:

- perfil financeiro (conservador, moderado, impulsivo)
- tolerância ao risco
- nível de comprometimento da renda
- Esses indicadores entram no prompt como contexto comportamental, não como dados pessoais brutos.

Transações Financeiras

Datasets:

transacoes.csv

Uso no prompt:
Os dados são analisados para identificar padrões de comportamento financeiro e gerar indicadores como:

- padrão de gastos recorrentes
- variações atípicas de valor ou frequência
- concentração de gastos por categoria
- Esses indicadores entram no prompt como sinais de alerta ou normalidade, não como histórico detalhado.

Movimentações Financeiras

Datasets:

movimentacoes.csv

Uso no prompt:
Os dados são analisados para avaliar fluxo financeiro e consistência das movimentações, gerando indicadores como:

- entradas vs. saídas de recursos
- possíveis inconsistências financeiras
- períodos de desequilíbrio no fluxo de caixa
- Esses indicadores entram no prompt como alertas de risco financeiro, não como registros individuais.

Detecção de fraude

Datasets:

credit_fraud_detection.parquet
financial_fraud_detection.csv

Uso no prompt:
Os dados são analisados para identificar padrões suspeitos e gerar indicadores como:

- nível de risco de fraude (baixo, médio, alto)
- probabilidade estimada de fraude
- tipo de risco detectado (transação fora do padrão, horário incomum, valor atípico)
- Esses indicadores entram no prompt como alertas de risco, não como dados brutos.

Análise de risco de crédito

Dataset:

credit_risk.csv

Uso no prompt:
Os dados são usados para classificar o usuário em faixas de risco de crédito, como:

- baixo, médio ou alto risco
- probabilidade de inadimplência
- perfil de comprometimento financeiro
- Essas classificações orientam o tom e o nível de cautela das respostas do agente.
- Perfil financeiro e comportamento de consumo

Datasets:

personal_finance_json.jsonl
personal_finance.parquet

Uso no prompt:
Os dados são utilizados para identificar padrões de comportamento, como:

- hábitos de consumo
- relação gasto vs. renda
- perfil financeiro (conservador, moderado, impulsivo)

Essas informações entram no prompt para contextualizar as respostas e evitar recomendações inadequadas ao perfil do usuário.

Forma final no prompt

No prompt, o agente recebe apenas informações consolidadas, por exemplo:

- “Risco de fraude: alto”
- “Perfil financeiro: impulsivo”
- “Risco de crédito: médio”

Esses dados são usados para:

- justificar alertas
- prevenir decisões impulsivas
- explicar riscos de forma clara
- garantir respostas seguras e coerentes
________________________________________________________________________________
Os dados são processados previamente para gerar indicadores de risco, classificações e perfis financeiros, que são então inseridos no prompt do agente como contexto resumido, permitindo respostas seguras, explicáveis e alinhadas ao papel do Guardião Financeiro.
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo do contexto montado abaixo, se baseia nos dados originais da base de conhecimento, que será extraido diretamente do site `Hugging Face`, mas serão sintetizados deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante que econimizar tokens, é ter todas as informações relevantes disponiveis em seu contexto.

## 1️⃣ Camada de Fraude Financeira
```text
Origem: df_credit_fraud_detection_parquet

🔧 Dados brutos (internos)

- amount
- saldo antes/depois
- tipo de ação (cash_in, cash_out, transfer…)
- flag de fraude

✅ Formato entregue ao agente (Brasil)
Análise de Transação:
- Tipo de operação: Saque
- Valor da transação: R$ 1.221.867,91
- Saldo antes da operação: R$ 1.221.867,91
- Saldo após a operação: R$ 0,00
- Comportamento identificado: Atípico
- Nível de risco de fraude: Alto

🌎 Formato (Usuário estrangeiro)

Transaction Analysis:
- Operation type: Cash Out
- Transaction amount: $1,221,867.91
- Balance before transaction: $1,221,867.91
- Balance after transaction: $0.00
- Detected behavior: Anomalous
- Fraud risk level: High
```
## 2️⃣ Camada de Classificação de Fraude (Texto Interpretado)

```text
Origem: df_financial_fraud_detection_csv

🔧 Dados brutos

- input
- response
- risk_classification

✅ Formato entregue ao agente (Brasil)
Classificação de Risco Financeiro:
- Situação analisada: Relação renda x dívida elevada
- Classificação de risco: Muito Alto
- Interpretação: A capacidade de pagamento atual é incompatível com o nível de endividamento.

🌎 Formato (Usuário estrangeiro)
Financial Risk Classification:
- Evaluated scenario: High debt-to-income ratio
- Risk classification: Very High
- Interpretation: Current income does not support existing debt obligations.
```

## 3️⃣ Camada de Risco de Crédito

```text
Origem: df_credit_risk_csv

✅ Formato entregue ao agente (Brasil)
Avaliação de Crédito:
- Nível de risco de crédito: Alto
- Probabilidade estimada de inadimplência: Elevada
- Recomendação do guardião: Ação cautelosa

🌎 Formato (Usuário estrangeiro)
Credit Risk Assessment:
- Credit risk level: High
- Estimated default probability: Elevated
- Guardian recommendation: Proceed with caution
```

## 4️⃣ Perfil Financeiro e Comportamento
```text
Origem:

df_personal_finance_json
df_personal_finance_parquet

🔧 Dados usados

- categoria (dívida, investimento, aposentadoria…)
- padrão de linguagem
- resposta aceita vs rejeitada

✅ Formato entregue ao agente (Brasil)
Perfil Financeiro do Usuário:
- Categoria dominante: Gestão de Dívidas
- Comportamento observado: Tendência a decisões emocionais
- Estilo de comunicação recomendado: Educativo e preventivo
- Perfil financeiro inferido: Impulsivo

🌎 Formato (Usuário estrangeiro)
User Financial Profile:
- Dominant category: Debt Management
- Observed behavior: Emotion-driven decisions
- Recommended communication style: Educational and preventive
- Inferred financial profile: Impulsive
```

## 5️⃣ Contexto Final Consolidado (o que vai para o prompt)
**🇧🇷 Brasil**
```text
Resumo do Guardião Financeiro:
- Risco de fraude: Alto
- Risco de crédito: Muito Alto
- Perfil financeiro: Impulsivo
- Ação recomendada: Alerta preventivo e explicação detalhada

🌍 Internacional
Financial Guardian Summary:
- Fraud risk: High
- Credit risk: Very High
- Financial profile: Impulsive
- Recommended action: Preventive alert with clear explanation
```
## 6️⃣ Camada de Perfil do Investidor
```text
Origem: perfil_investidor.json

🔧 Dados brutos (internos)

- renda mensal
- tolerância ao risco
- histórico financeiro
- objetivo financeiro

✅ Formato entregue ao agente

Perfil Financeiro:

- Tipo de perfil: Impulsivo
- Tolerância ao risco: Baixa
- Estabilidade financeira: Média
- Grau de comprometimento de renda: Alto
```

## 7️⃣ Camada de Transações Financeiras
```text
Origem: transacoes.csv

🔧 Dados brutos (internos)

- data da transação
- categoria
- valor
- tipo (entrada / saída)

✅ Formato entregue ao agente

Padrão de Transações:

- Frequência de gastos: Alta
- Categoria dominante: Consumo
- Variação de valores: Elevada
- Comportamento financeiro: Inconsistente
```

## 8️⃣ Camada de Movimentações Financeiras
```text
Origem: movimentacoes.csv

🔧 Dados brutos (internos)

- entradas e saídas
- saldo acumulado
- períodos de desequilíbrio

✅ Formato entregue ao agente

Fluxo Financeiro:

- Relação entradas vs. saídas: Desfavorável
- Períodos de desequilíbrio: Frequentes
- Tendência financeira: Risco de descontrole
- Nível de alerta financeiro: Médio
```