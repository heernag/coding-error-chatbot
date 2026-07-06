from time import perf_counter


def _now() -> str:
    return f"{perf_counter():.6f}"


def log_event(message: str) -> None:
    print(f"[CHAT DIAG] t={_now()} {message}", flush=True)


def log_duration(step: str, elapsed_seconds: float) -> None:
    print(f"[CHAT DIAG] {step} elapsed={elapsed_seconds:.3f}s", flush=True)


def log_llm_settings(settings) -> None:
    api_key_loaded = bool(getattr(settings, "OPENROUTER_API_KEY", None))
    base_url = getattr(settings, "OPENROUTER_BASE_URL", "")
    model = getattr(settings, "OPENROUTER_MODEL", "")

    print(
        "[CHAT DIAG] OpenRouter settings "
        f"api_key_loaded={api_key_loaded} "
        f"base_url={base_url} "
        f"model={model}",
        flush=True,
    )
