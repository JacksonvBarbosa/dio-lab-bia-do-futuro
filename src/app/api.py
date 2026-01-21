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

