import requests
import os
from src.agent.system_prompt import SYSTEM_PROMPT

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HF_TOKEN")


def perguntar_fortis_hf(pergunta_usuario: str, contexto: str) -> str:
    """
    Envia a pergunta para o agente Fortis usando Hugging Face Inference API.
    """

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

PERGUNTA DO USUÁRIO:
{pergunta_usuario}
"""

    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result[0]["generated_text"].strip()
