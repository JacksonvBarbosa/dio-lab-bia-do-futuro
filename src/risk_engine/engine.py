from .fraud_detection import avaliar_fraude
from .credit_risk import avaliar_credito
from .financial_profile import avaliar_perfil


def gerar_sinais_risco(perfil, transacoes, movimentacoes):
    return {
        "fraude": avaliar_fraude(transacoes, movimentacoes),
        "credito": avaliar_credito(perfil, movimentacoes),
        "comportamento": avaliar_perfil(transacoes, movimentacoes)
    }
