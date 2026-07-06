import importlib
import sys
import types
import unittest


EXPECTED_SECTIONS = [
    "[오류 요약]",
    "[원인]",
    "[진단 방법]",
    "[해결 방법]",
    "[수정 코드 예시]",
    "[주의사항]",
]


class RagServiceFormatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        vector_db = types.ModuleType("app.services.vector_db")
        vector_db.data = []
        vector_db.vectorstore = object()

        llm_service = types.ModuleType("app.services.llm_service")
        llm_service.invoke_with_fallback = lambda prompt: types.SimpleNamespace(content="")

        sys.modules["app.services.vector_db"] = vector_db
        sys.modules["app.services.llm_service"] = llm_service
        cls.rag_service = importlib.import_module("app.services.rag_service")

    def test_no_context_response_uses_required_sections(self):
        response = self.rag_service.build_no_context_response(
            "ModuleNotFoundError: no module named pandas"
        )

        last_index = -1
        for section in EXPECTED_SECTIONS:
            index = response.find(section)
            self.assertGreater(index, last_index)
            last_index = index

    def test_answer_prompt_limits_answer_to_retrieved_context(self):
        prompt = self.rag_service.build_answer_prompt("question", "retrieved document")

        self.assertIn(EXPECTED_SECTIONS[0], prompt)
        self.assertIn(EXPECTED_SECTIONS[2], prompt)
        self.assertIn("retrieved document", prompt)
        self.assertIn("question", prompt)


class RagServiceDocumentMatchTest(unittest.TestCase):
    def test_document_match_returns_required_sections_without_llm_call(self):
        vector_db = types.ModuleType("app.services.vector_db")
        vector_db.data = []
        vector_db.vectorstore = object()

        llm_service = types.ModuleType("app.services.llm_service")
        llm_service.invoke_with_fallback = lambda prompt: types.SimpleNamespace(content="")

        sys.modules["app.services.vector_db"] = vector_db
        sys.modules["app.services.llm_service"] = llm_service
        sys.modules.pop("app.services.rag_service", None)
        rag_service = importlib.import_module("app.services.rag_service")

        class FakeDoc:
            metadata = {
                "title": "ModuleNotFoundError",
                "description": "module import error",
                "category": "Python",
                "subcategory": "Package",
                "error_code": "",
                "cause": "missing package",
                "diagnosis": "check package",
                "solution": "install package",
                "examples": "pip install pandas",
                "command_example": "python -m pip show pandas",
                "caution": "check virtual environment",
                "source_url": "",
            }

        class FakeRetriever:
            def invoke(self, question):
                return [FakeDoc()]

        class FakeVectorstore:
            def as_retriever(self, **kwargs):
                return FakeRetriever()

        original_vectorstore = rag_service.vectorstore
        original_invoke_with_fallback = rag_service.invoke_with_fallback
        rag_service.vectorstore = FakeVectorstore()
        rag_service.invoke_with_fallback = lambda prompt: (_ for _ in ()).throw(
            AssertionError("LLM should not be called when a document was found")
        )

        try:
            response = rag_service.get_rag_answer("pandas import error", "test-session")
        finally:
            rag_service.vectorstore = original_vectorstore
            rag_service.invoke_with_fallback = original_invoke_with_fallback

        for section in EXPECTED_SECTIONS:
            self.assertIn(section, response)
        self.assertIn("pip install pandas", response)
        self.assertIn("python -m pip show pandas", response)


if __name__ == "__main__":
    unittest.main()
