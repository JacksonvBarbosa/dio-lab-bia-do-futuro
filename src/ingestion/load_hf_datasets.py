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
