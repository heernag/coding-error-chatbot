import io
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace


class DiagnosticsTest(unittest.TestCase):
    def test_llm_settings_log_masks_secret_values(self):
        from app.services.diagnostics import log_llm_settings

        settings = SimpleNamespace(
            OPENROUTER_API_KEY="sk-or-secret-value",
            OPENROUTER_BASE_URL="https://openrouter.ai/api/v1",
            OPENROUTER_MODEL="google/gemma-4-26b-a4b-it:free",
        )

        output = io.StringIO()
        with redirect_stdout(output):
            log_llm_settings(settings)

        logs = output.getvalue()

        self.assertIn("api_key_loaded=True", logs)
        self.assertIn("base_url=https://openrouter.ai/api/v1", logs)
        self.assertIn("model=google/gemma-4-26b-a4b-it:free", logs)
        self.assertNotIn("sk-or-secret-value", logs)

    def test_log_duration_prints_named_step(self):
        from app.services.diagnostics import log_duration

        output = io.StringIO()
        with redirect_stdout(output):
            log_duration("LLM call", 1.234)

        logs = output.getvalue()

        self.assertIn("LLM call", logs)
        self.assertIn("1.234s", logs)


if __name__ == "__main__":
    unittest.main()
