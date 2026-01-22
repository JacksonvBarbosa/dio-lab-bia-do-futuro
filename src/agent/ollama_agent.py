import requests
from src.agent.system_prompt import SYSTEM_PROMPT

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b"  # ajuste para o modelo que estiver rodando no Ollama


def perguntar_fortis_ollama(pergunta_usuario: str, contexto: str) -> str:
    """
    Envia a pergunta para o agente Fortis via Ollama.
    """

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

PERGUNTA DO USUÁRIO:
{pergunta_usuario}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json().get("response", "").strip()
