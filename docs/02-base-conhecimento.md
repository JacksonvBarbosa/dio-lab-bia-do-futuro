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

## Os dados externos do site Hugging face serão carregados via Data Connector ou Data Adapter.

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

## O sistema irá consumir diretamente chamando a função com os dados especificos.

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

# Os arquivos internos da pasta `data/raw` serão consumidos ou via código ou injetando os dados diretamente no prompt (Ctrl + c, Ctrl + v)

```python
import pandas as pd
from pathlib import Path

# Caminho base dos dados
DATA_RAW_PATH = Path("data/raw")

# 1️⃣ Perfil do Investidor (JSON)
df_perfil_investidor = pd.read_json(
    DATA_RAW_PATH / "perfil_investidor.json"
)

# 2️⃣ Transações Financeiras (CSV)
df_transacoes = pd.read_csv(
    DATA_RAW_PATH / "transacoes.csv"
)

# 3️⃣ Movimentações Financeiras (CSV)
df_movimentacoes = pd.read_csv(
    DATA_RAW_PATH / "movimentacoes.csv"
)

# Verificação rápida
print("Perfil Investidor:", df_perfil_investidor.shape)
print("Transações:", df_transacoes.shape)
print("Movimentações:", df_movimentacoes.shape)

```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados serão parte injetado com dados estáticos para uma fácil compreensão e usabilidade no projeto sendo consumido via código ou diretamente pelo prompt.
Lembrando que em soluções mais robustas, o ideal é que esses dados sejam carregados dinamicamente como estão sendo carregados os dados via Data Connector direto do site Hugging Face, essa solução de Data Connector também pode usado com S3(`s3://`), GCS(`gs://`), Azure Blob(`abfs://`).
Enfim o projeto está pronto para ser escalado a um projeto com mais robustes.

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
```
#### Esse é o formato do arquivo extraido do arquivo perfil_investidor.json.
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>investidor_id</th>
      <th>nome</th>
      <th>idade</th>
      <th>profissao</th>
      <th>renda_mensal</th>
      <th>perfil_investidor</th>
      <th>objetivo_principal</th>
      <th>patrimonio_total</th>
      <th>reserva_emergencia_atual</th>
      <th>aceita_risco</th>
      <th>metas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>João Silva</td>
      <td>32</td>
      <td>Analista de Sistemas</td>
      <td>5000</td>
      <td>moderado</td>
      <td>Construir reserva de emergência</td>
      <td>15000</td>
      <td>10000</td>
      <td>False</td>
      <td>[{'meta': 'Completar reserva de emergência', '...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Maria Oliveira</td>
      <td>28</td>
      <td>Designer</td>
      <td>4200</td>
      <td>conservador</td>
      <td>Organizar finanças pessoais</td>
      <td>8000</td>
      <td>3000</td>
      <td>False</td>
      <td>[{'meta': 'Reserva de emergência', 'valor_nece...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Carlos Mendes</td>
      <td>45</td>
      <td>Gerente Comercial</td>
      <td>9500</td>
      <td>moderado</td>
      <td>Aposentadoria</td>
      <td>220000</td>
      <td>40000</td>
      <td>True</td>
      <td>[{'meta': 'Aumentar patrimônio para aposentado...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Ana Costa</td>
      <td>35</td>
      <td>Empreendedora</td>
      <td>12000</td>
      <td>arrojado</td>
      <td>Crescimento patrimonial</td>
      <td>180000</td>
      <td>30000</td>
      <td>True</td>
      <td>[{'meta': 'Diversificar investimentos', 'valor...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Pedro Santos</td>
      <td>22</td>
      <td>Estudante</td>
      <td>1800</td>
      <td>conservador</td>
      <td>Educação financeira</td>
      <td>2000</td>
      <td>500</td>
      <td>False</td>
      <td>[{'meta': 'Criar reserva inicial', 'valor_nece...</td>
    </tr>
  </tbody>
</table>
</div>

```text
Transações Financeiras

Datasets: transacoes.csv

Uso no prompt:
Os dados são analisados para identificar padrões de comportamento financeiro e gerar indicadores como:

- padrão de gastos recorrentes
- variações atípicas de valor ou frequência
- concentração de gastos por categoria
- Esses indicadores entram no prompt como sinais de alerta ou normalidade, não como histórico detalhado.
```

#### Esse é o formato do arquivo extraido do arquivo transacoes.csv
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>data</th>
      <th>descricao</th>
      <th>categoria</th>
      <th>valor</th>
      <th>tipo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2025-10-01</td>
      <td>Salário</td>
      <td>receita</td>
      <td>5000.0</td>
      <td>entrada</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2025-10-02</td>
      <td>Aluguel</td>
      <td>moradia</td>
      <td>1200.0</td>
      <td>saida</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2025-10-03</td>
      <td>Supermercado</td>
      <td>alimentacao</td>
      <td>450.0</td>
      <td>saida</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2025-10-05</td>
      <td>Netflix</td>
      <td>lazer</td>
      <td>55.9</td>
      <td>saida</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2025-10-07</td>
      <td>Farmácia</td>
      <td>saude</td>
      <td>89.0</td>
      <td>saida</td>
    </tr>
  </tbody>
</table>
</div>

```text
Movimentações Financeiras

Datasets: movimentacoes.csv

Uso no prompt: Os dados são analisados para avaliar fluxo financeiro e consistência das movimentações, gerando indicadores como:

- entradas vs. saídas de recursos
- possíveis inconsistências financeiras
- períodos de desequilíbrio no fluxo de caixa
- Esses indicadores entram no prompt como alertas de risco financeiro, não como registros individuais.
```

#### Esse é o formato do arquivo extraido do arquivo movimentacoes.csv
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>movimentacao_id</th>
      <th>investidor_id</th>
      <th>data_movimentacao</th>
      <th>descricao</th>
      <th>categoria</th>
      <th>tipo</th>
      <th>valor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>2025-10-01</td>
      <td>Salário</td>
      <td>receita</td>
      <td>entrada</td>
      <td>5000.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>2025-10-02</td>
      <td>Aluguel</td>
      <td>moradia</td>
      <td>saida</td>
      <td>1200.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>2025-10-01</td>
      <td>Salário</td>
      <td>receita</td>
      <td>entrada</td>
      <td>4200.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2</td>
      <td>2025-10-05</td>
      <td>Supermercado</td>
      <td>alimentacao</td>
      <td>saida</td>
      <td>600.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3</td>
      <td>2025-10-01</td>
      <td>Salário</td>
      <td>receita</td>
      <td>entrada</td>
      <td>9500.0</td>
    </tr>
  </tbody>
</table>
</div>

## Dados externos do Hugging Face
```text
Detecção de fraude

Datasets Externo:

credit_fraud_detection.parquet
financial_fraud_detection.csv

Uso no prompt: Os dados são analisados para identificar padrões suspeitos e gerar indicadores como:

- nível de risco de fraude (baixo, médio, alto)
- probabilidade estimada de fraude
- tipo de risco detectado (transação fora do padrão, horário incomum, valor atípico)
- Esses indicadores entram no prompt como alertas de risco, não como dados brutos.

#==========================================================================#

Análise de risco de crédito

Dataset Externo: credit_risk.csv

Uso no prompt: Os dados são usados para classificar o usuário em faixas de risco de crédito, como:

- baixo, médio ou alto risco
- probabilidade de inadimplência
- perfil de comprometimento financeiro
- Essas classificações orientam o tom e o nível de cautela das respostas do agente.
- Perfil financeiro e comportamento de consumo

Datasets Externo:

personal_finance_json.jsonl
personal_finance.parquet

Uso no prompt: Os dados são utilizados para identificar padrões de comportamento, como:

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

O exemplo do contexto montado abaixo, se baseia nos dados internos da base de conhecimento, e também serão extraidos diretamente do site `Hugging Face` dados para averiguações estatísticas que se refere a possíveis movimentações e ações de fraude, os dados serão sintetizados deixando apenas as informações mais relevantes, otimizando assim o consumo de tokens. Entretanto, vale lembrar que mais importante que econimizar tokens, é ter todas as informações relevantes disponiveis em seu contexto.

## 🧍‍♂️ DADOS DO CLIENTE (INTERNOS)
```text
Identificação do Cliente:
- Nome: João Silva
- Perfil financeiro: Impulsivo
- Objetivo financeiro: Aumentar renda mantendo segurança
- Tolerância ao risco: Baixa
- Estabilidade financeira: Média
- Reserva atual: R$ 15.000
- Meta de reserva: R$ 25.000
```
## 💳 RESUMO DE GASTOS E MOVIMENTAÇÕES

```text
Resumo Financeiro Recente:
- Moradia: R$ 2.100
- Alimentação: R$ 1.450
- Transporte: R$ 620
- Saúde: R$ 310
- Lazer: R$ 980
- Total de gastos mensais: R$ 5.460

Fluxo Financeiro:
- Relação entradas vs. saídas: Desfavorável
- Frequência de desequilíbrio: Frequente
- Tendência observada: Risco de descontrole
```

## 🔍 ANÁLISE DE TRANSAÇÃO ESPECÍFICA (FRAUDE)

```text
Análise de Transação:
- Tipo de operação: Saque
- Valor da transação: R$ 48.900
- Horário: Noturno
- Comportamento identificado: Fora do padrão histórico
- Nível de risco de fraude: Alto
```

## 📉 AVALIAÇÃO DE RISCO DE CRÉDITO (BASE EXTERNA)
```text
Avaliação de Crédito:
- Nível de risco de crédito: Alto
- Probabilidade estimada de inadimplência: Elevada
- Principal fator de risco: Alto comprometimento de renda
```

## 🧠 PERFIL COMPORTAMENTAL INFERIDO
```text
Perfil Comportamental:
- Tendência dominante: Decisões emocionais sob pressão
- Reação a alertas: Parcialmente responsiva
- Estilo de comunicação recomendado: Educativo e preventivo
```

## ⚠️ TIPOS DE RISCOS IDENTIFICADOS
```text
Mapa de Riscos:
- Risco de fraude: Alto
- Risco de crédito: Alto
- Risco de descontrole financeiro: Médio
- Risco de decisão impulsiva: Elevado
```

## 🛡️ CONTEXTO FINAL CONSOLIDADO (ENVIADO AO PROMPT)
```text
Resumo do Guardião Financeiro Fortis:
- Perfil: Impulsivo
- Reserva abaixo da meta
- Fluxo financeiro instável
- Risco de fraude elevado em transação recente
- Risco de crédito elevado
- Ação sugerida: Alerta preventivo com explicação clara e orientação segura

```

## 📌 Observação Importante

- O agente não recebe dados brutos
- Bases do Hugging Face são usadas apenas como referência estatística
- O prompt contém sinais, classificações e alertas
- Isso reduz tokens, evita alucinação e mantém o Fortis dentro do escopo legal e ético