from .fraud_detection import avaliar_fraude
from .credit_risk import avaliar_credito
from .financial_profile import avaliar_perfil

def gerar_sinais_risco(transacoes, movimentacoes, perfil):
    fraude = avaliar_fraude(transacoes, movimentacoes)
    credito = avaliar_credito(perfil, movimentacoes)
    perfil_fin = avaliar_perfil(transacoes, movimentacoes)

    alerta_principal = (
        fraude["motivos"][0]
        if fraude["motivos"]
        else credito["fatores_chave"][0]
        if credito["fatores_chave"]
        else "Nenhum alerta crítico identificado"
    )

    return {
        "fraude": fraude["fraude_risco"],
        "credito": credito["credito_risco"],
        "comportamento": perfil_fin["perfil_financeiro"],
        "alerta_principal": alerta_principal,
        "acao_recomendada": fraude["acao_sugerida"]
    }
