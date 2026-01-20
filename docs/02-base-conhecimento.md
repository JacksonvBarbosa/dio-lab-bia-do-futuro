# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `credit_fraud_detection.parquet` e `financial_fraud_detection.csv` | Parquet | Análisa padrões de possiveis ações fraudulentas, excelente para camada de risco |
| `credit_risk.csv` | csv | Avalia o risco de crédito, inferi probabilidade de inadimplência e classifica usuários por nível de risco |
| `personal_finance_json.jsonl` e `personal_finance.parquet` | json | Identifica hábitos de consumo, entende padrões de gasto vs. renda e inferi perfil financeiro (conservador, moderado, impulsivo, etc.) |

---

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

**Nota:** Crie um arquivo data_loader.py, dentro da pasta src e insira o código nele para cria uma classe Dataloader sendo mais fácil de ser manipulada.

```python
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw")


class DataLoader:
    def __init__(self, base_path: Path = DATA_PATH):
        self.base_path = base_path

    def load_parquet(self, filename: str) -> pd.DataFrame:
        path = self.base_path / filename
        return pd.read_parquet(path)

    def load_csv(self, filename: str) -> pd.DataFrame:
        path = self.base_path / filename
        return pd.read_csv(path)

    def load_jsonl(self, filename: str) -> pd.DataFrame:
        path = self.base_path / filename
        return pd.read_json(path, lines=True, encoding='utf-8')

    def load_all(self) -> dict:
        return {
            "credit_fraud": self.load_parquet("credit_fraud_detection.parquet"),
            "financial_fraud": self.load_csv("financial_fraud_detection.csv"),
            "credit_risk": self.load_csv("credit_risk.csv"),
            "personal_finance": self.load_parquet("personal_finance.parquet"),
            "personal_profile": self.load_jsonl("personal_finance_json.jsonl"),
        }

```

```python
# Exemplo de como usar no projeto

from src.data_loader import DataLoader

loader = DataLoader()
datasets = loader.load_all()

df_fraud = datasets["credit_fraud"]
df_risk = datasets["credit_risk"]
df_profile = datasets["personal_profile"]

print(df_fraud.shape)
print(df_risk.head())

```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

```text
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

hábitos de consumo

relação gasto vs. renda

perfil financeiro (conservador, moderado, impulsivo)

Essas informações entram no prompt para contextualizar as respostas e evitar recomendações inadequadas ao perfil do usuário.

Forma final no prompt

No prompt, o agente recebe apenas informações consolidadas, por exemplo:

“Risco de fraude: alto”

“Perfil financeiro: impulsivo”

“Risco de crédito: médio”

Esses dados são usados para:

justificar alertas

prevenir decisões impulsivas

explicar riscos de forma clara

garantir respostas seguras e coerentes
________________________________________________________________________________
Os dados são processados previamente para gerar indicadores de risco, classificações e perfis financeiros, que são então inseridos no prompt do agente como contexto resumido, permitindo respostas seguras, explicáveis e alinhadas ao papel do Guardião Financeiro.
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo do contexto montado abaixo, se baseia nos dados originais da base de conhecimento, mas os siinteiza deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante que econimizar tokens, é ter todas as informações relevantes disponiveis em seu contexto.

## 1️⃣ Camada de Fraude Financeira
```text
Origem: credit_fraud_detection.parquet

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
Origem: df_cred_fraud_dec

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
Origem: credit_risk.csv

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

personal_finance_json.jsonl
personal_finance.parquet

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