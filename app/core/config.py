import os

from dotenv import load_dotenv

load_dotenv()


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings:
    PROJECT_NAME: str = "코딩 오류 분석 챗봇"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    OPENROUTER_API_KEY: str | None = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "poolside/laguna-xs-2.1:free")
    OPENROUTER_FALLBACK_MODELS: list[str] = _parse_csv(
        os.getenv(
            "OPENROUTER_FALLBACK_MODELS",
            "nvidia/nemotron-3-nano-30b-a3b:free,openai/gpt-oss-20b:free,cohere/north-mini-code:free,google/gemma-4-26b-a4b-it:free",
        )
    )
    OPENROUTER_HTTP_REFERER: str | None = os.getenv("OPENROUTER_HTTP_REFERER")
    OPENROUTER_APP_TITLE: str = os.getenv("OPENROUTER_APP_TITLE", "Coding Error Chatbot")


settings = Settings()
