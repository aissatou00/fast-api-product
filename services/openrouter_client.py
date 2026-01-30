import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "upstage/solar-pro-3:free")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_APP_NAME = os.getenv("OPENROUTER_APP_NAME", "fastapi-app")
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "http://localhost")


class OpenRouterError(RuntimeError):
    pass


async def chat_completion(messages: list[dict], temperature: float = 0.2) -> str:
    if not OPENROUTER_API_KEY:
        raise OpenRouterError(
            "OPENROUTER_API_KEY manquante dans le .env"
        )

    url = f"{OPENROUTER_BASE_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": OPENROUTER_APP_NAME,
        "HTTP-Referer": OPENROUTER_SITE_URL,
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": temperature,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code >= 400:
        raise OpenRouterError(f"OpenRouter error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]
