# from openai import OpenAI
# from src.agent.system_prompt import SYSTEM_PROMPT

# client = OpenAI()


# def perguntar_fortis_openai(pergunta_usuario: str, contexto: str) -> str:
#     """
#     Envia a pergunta para o agente Fortis usando OpenAI.
#     """

#     messages = [
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "system", "content": f"CONTEXTO DO CLIENTE:\n{contexto}"},
#         {"role": "user", "content": pergunta_usuario}
#     ]

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",  # ou outro modelo
#         messages=messages,
#         temperature=0.2
#     )

#     return response.choices[0].message.content.strip()
