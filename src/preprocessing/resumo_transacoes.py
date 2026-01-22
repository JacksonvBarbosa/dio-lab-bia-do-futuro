def resumir_transacoes(df):
    return {
        "categoria_dominante": df["categoria"].mode()[0],
        "media_mensal": round(df["valor"].mean(), 2),
        "frequencia": "Alta" if len(df) > 30 else "Moderada",
        "comportamento": "Inconsistente" if df["valor"].std() > 1000 else "Estável"
    }
