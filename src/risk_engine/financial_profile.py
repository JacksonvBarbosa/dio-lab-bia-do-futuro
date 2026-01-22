def avaliar_perfil(transacoes, movimentacoes):
    variacao = transacoes["valor"].std()
    frequencia = len(transacoes)

    comportamentos = []
    if variacao > transacoes["valor"].mean():
        comportamentos.append("Alta variação nos valores gastos")

    if frequencia > 20:
        comportamentos.append("Alta frequência de transações")

    perfil = "Impulsivo" if comportamentos else "Controlado"

    return {
        "perfil_financeiro": perfil,
        "estabilidade": "Baixa" if perfil == "Impulsivo" else "Alta",
        "comportamentos": comportamentos,
        "tom_recomendado": "Educativo e preventivo" if perfil == "Impulsivo" else "Informativo"
    }
