def montar_contexto_fortis(
    perfil_investidor: dict,
    resumo_transacoes: dict,
    resumo_movimentacoes: dict,
    sinais_risco: dict
) -> str:
    """
    Monta o contexto final enviado ao agente Fortis.
    """
    contexto = f"""
RESUMO DO CLIENTE:
- Nome: {perfil_investidor.get('nome')}
- Perfil financeiro declarado: {perfil_investidor.get('perfil_investidor')}
- Objetivo financeiro: {perfil_investidor.get('objetivo_principal')}
- Tolerância ao risco: {"Sim" if perfil_investidor.get('aceita_risco') else "Não"}
- Reserva atual: R$ {perfil_investidor.get('reserva_emergencia_atual')}
- Meta de reserva: R$ {sum(meta.get('valor_necessario', 0) for meta in perfil_investidor.get('metas', []))}

RESUMO DE GASTOS E TRANSAÇÕES:
- Categoria dominante de gastos: {resumo_transacoes.get('categoria_dominante')}
- Média mensal de gastos: R$ {resumo_transacoes.get('media_mensal')}
- Frequência de gastos: {resumo_transacoes.get('frequencia')}
- Comportamento financeiro observado: {resumo_transacoes.get('comportamento')}

FLUXO FINANCEIRO:
- Relação entre entradas e saídas: {resumo_movimentacoes.get('relacao')}
- Estabilidade financeira: {resumo_movimentacoes.get('estabilidade')}
- Tendência recente do fluxo: {resumo_movimentacoes.get('tendencia')}

SINAIS DE RISCO (ANÁLISE ESTATÍSTICA):
- Risco de fraude: {sinais_risco.get('fraude')}
- Risco de crédito: {sinais_risco.get('credito')}
- Risco comportamental: {sinais_risco.get('comportamento')}
- Alerta principal: {sinais_risco.get('alerta_principal')}

NÍVEL GERAL DE ALERTA:
- Classificação: {sinais_risco.get('acao_recomendada')}

ORIENTAÇÃO DO GUARDIÃO FINANCEIRO:
- Alertar riscos identificados
- Explicar impactos financeiros de forma clara
- Orientar comportamento preventivo
- NÃO recomendar investimentos específicos
- NÃO tomar decisões financeiras pelo cliente
"""
    return contexto.strip()
