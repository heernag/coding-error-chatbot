import importlib
import os
import sys
import types
import unittest


class LlmServiceConfigTest(unittest.TestCase):
    def setUp(self):
        for module_name in ["app.core.config", "app.services.llm_service"]:
            sys.modules.pop(module_name, None)
        sys.modules.pop("langchain_openai", None)
        os.environ.pop("OPENROUTER_FALLBACK_MODELS", None)

    def test_settings_use_openrouter_environment(self):
        os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
        os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1"
        os.environ["OPENROUTER_MODEL"] = "cohere/north-mini-code:free"
        os.environ["OPENROUTER_FALLBACK_MODELS"] = (
            "cohere/north-mini-code:free, poolside/laguna-xs-2.1:free"
        )

        config = importlib.import_module("app.core.config")

        self.assertEqual(config.settings.OPENROUTER_API_KEY, "test-openrouter-key")
        self.assertEqual(config.settings.OPENROUTER_BASE_URL, "https://openrouter.ai/api/v1")
        self.assertEqual(config.settings.OPENROUTER_MODEL, "cohere/north-mini-code:free")
        self.assertEqual(
            config.settings.OPENROUTER_FALLBACK_MODELS,
            ["cohere/north-mini-code:free", "poolside/laguna-xs-2.1:free"],
        )

    def test_llm_service_configures_chatopenai_for_openrouter(self):
        os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
        os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1"
        os.environ["OPENROUTER_MODEL"] = "cohere/north-mini-code:free"
        os.environ["OPENROUTER_FALLBACK_MODELS"] = ""

        captured = {}
        fake_langchain_openai = types.ModuleType("langchain_openai")

        class FakeChatOpenAI:
            def __init__(self, **kwargs):
                captured.update(kwargs)

        fake_langchain_openai.ChatOpenAI = FakeChatOpenAI
        sys.modules["langchain_openai"] = fake_langchain_openai

        importlib.import_module("app.services.llm_service")

        self.assertEqual(captured["model"], "cohere/north-mini-code:free")
        self.assertEqual(captured["api_key"], "test-openrouter-key")
        self.assertEqual(captured["base_url"], "https://openrouter.ai/api/v1")
        self.assertEqual(captured["temperature"], 0.2)
        self.assertEqual(captured["timeout"], 60)
        self.assertEqual(captured["max_retries"], 0)
        self.assertEqual(captured["max_tokens"], 700)
        self.assertEqual(captured["default_headers"]["X-OpenRouter-Title"], "Coding Error Chatbot")

    def test_llm_service_retries_next_openrouter_model(self):
        os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
        os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1"
        os.environ["OPENROUTER_MODEL"] = "first/free-model:free"
        os.environ["OPENROUTER_FALLBACK_MODELS"] = "second/free-model:free"

        calls = []
        fake_langchain_openai = types.ModuleType("langchain_openai")

        class FakeChatOpenAI:
            def __init__(self, **kwargs):
                self.model = kwargs["model"]

            def invoke(self, prompt):
                calls.append(self.model)
                if self.model == "first/free-model:free":
                    raise RuntimeError("rate limit")
                return types.SimpleNamespace(content="fallback ok")

        fake_langchain_openai.ChatOpenAI = FakeChatOpenAI
        sys.modules["langchain_openai"] = fake_langchain_openai

        llm_service = importlib.import_module("app.services.llm_service")
        response = llm_service.invoke_with_fallback("hello")

        self.assertEqual(response.content, "fallback ok")
        self.assertEqual(calls, ["first/free-model:free", "second/free-model:free"])

    def test_llm_service_retries_when_model_returns_empty_content(self):
        os.environ["OPENROUTER_API_KEY"] = "test-openrouter-key"
        os.environ["OPENROUTER_BASE_URL"] = "https://openrouter.ai/api/v1"
        os.environ["OPENROUTER_MODEL"] = "empty/free-model:free"
        os.environ["OPENROUTER_FALLBACK_MODELS"] = "second/free-model:free"

        calls = []
        fake_langchain_openai = types.ModuleType("langchain_openai")

        class FakeChatOpenAI:
            def __init__(self, **kwargs):
                self.model = kwargs["model"]

            def invoke(self, prompt):
                calls.append(self.model)
                if self.model == "empty/free-model:free":
                    return types.SimpleNamespace(content="")
                return types.SimpleNamespace(content="fallback ok")

        fake_langchain_openai.ChatOpenAI = FakeChatOpenAI
        sys.modules["langchain_openai"] = fake_langchain_openai

        llm_service = importlib.import_module("app.services.llm_service")
        response = llm_service.invoke_with_fallback("hello")

        self.assertEqual(response.content, "fallback ok")
        self.assertEqual(calls, ["empty/free-model:free", "second/free-model:free"])


if __name__ == "__main__":
    unittest.main()
