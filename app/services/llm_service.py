from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.services.diagnostics import log_event


default_headers = {
    "X-OpenRouter-Title": settings.OPENROUTER_APP_TITLE,
}

if settings.OPENROUTER_HTTP_REFERER:
    default_headers["HTTP-Referer"] = settings.OPENROUTER_HTTP_REFERER


def _model_names() -> list[str]:
    names = [settings.OPENROUTER_MODEL, *settings.OPENROUTER_FALLBACK_MODELS]
    unique_names = []
    for name in names:
        if name and name not in unique_names:
            unique_names.append(name)
    return unique_names


def create_llm(model: str) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        temperature=0.2,
        default_headers=default_headers,
        timeout=60,
        max_retries=0,
        max_tokens=700,
    )


llms = [(model, create_llm(model)) for model in _model_names()]
llm = llms[0][1]


def invoke_with_fallback(prompt: str):
    last_error = None
    for model, candidate_llm in llms:
        try:
            log_event(f"OpenRouter model attempt model={model}")
            response = candidate_llm.invoke(prompt)
            if not str(getattr(response, "content", "")).strip():
                raise ValueError("empty model response")
            return response
        except Exception as e:
            last_error = e
            log_event(f"OpenRouter model failed model={model} error_type={type(e).__name__}")

    if last_error:
        raise last_error
    raise RuntimeError("No OpenRouter models configured")
