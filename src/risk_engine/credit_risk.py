def avaliar_credito(perfil_investidor, movimentacoes):
    """
    Avalia risco de crédito para um investidor.
    perfil_investidor: dict (um investidor da lista)
    movimentacoes: DataFrame
    """
    renda = perfil_investidor.get("renda_mensal", 0)
    gastos = movimentacoes["valor"].sum()

    comprometimento = gastos / renda if renda > 0 else 1

    fatores = []
    if comprometimento > 0.6:
        fatores.append("Comprometimento elevado da renda")

    if perfil_investidor.get("reserva_emergencia_atual", 0) < renda * 3:
        fatores.append("Reserva abaixo do recomendado")

    risco = "Alto" if len(fatores) >= 2 else "Médio" if fatores else "Baixo"

    return {
        "credito_risco": risco,
        "inadimplencia": "Provável" if risco == "Alto" else "Possível",
        "fatores_chave": fatores,
        "nivel_alerta": "Atenção" if risco != "Baixo" else "Normal"
    }
