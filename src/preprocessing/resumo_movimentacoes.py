def resumir_movimentacoes(df):
    entradas = df[df["tipo"] == "entrada"]["valor"].sum()
    saidas = df[df["tipo"] == "saida"]["valor"].sum()

    relacao = "Desfavorável" if saidas > entradas else "Equilibrada"

    return {
        "relacao": relacao,
        "estabilidade": "Baixa" if abs(entradas - saidas) > 5000 else "Alta",
        "tendencia": "Risco de descontrole" if saidas > entradas else "Sob controle"
    }
