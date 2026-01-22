def avaliar_fraude(transacoes, movimentacoes):
    sinais = []

    # Valor fora do padrão histórico
    if transacoes["valor"].max() > transacoes["valor"].mean() * 3:
        sinais.append("Valor muito acima do padrão histórico")

    # Transação noturna (se existir a coluna)
    if "noturno" in transacoes.columns and transacoes["noturno"].any():
        sinais.append("Transação em horário incomum")

    # Checar se há movimentações negativas
    if (movimentacoes["valor"] < 0).any():
        sinais.append("Existem movimentações negativas")

    # Classificação do risco
    risco = "Alto" if len(sinais) >= 2 else "Médio" if sinais else "Baixo"

    return {
        "fraude_risco": risco,
        "probabilidade": "Elevada" if risco == "Alto" else "Moderada",
        "motivos": sinais,
        "acao_sugerida": "Alerta preventivo" if risco != "Baixo" else "Monitoramento"
    }
