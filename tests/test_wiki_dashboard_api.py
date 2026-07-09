import unittest
from datetime import datetime
import sys
import types

from fastapi.testclient import TestClient

vector_db = types.ModuleType("app.services.vector_db")
vector_db.data = []
vector_db.vectorstore = object()

llm_service = types.ModuleType("app.services.llm_service")
llm_service.invoke_with_fallback = lambda prompt: types.SimpleNamespace(content="")

sys.modules["app.services.vector_db"] = vector_db
sys.modules["app.services.llm_service"] = llm_service

from app.database.connection import get_db
from app.database.models import ChatHistory
from app.main import app
from app.services import wiki_service


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows

    def count(self):
        return len(self.rows)

    def filter(self, *args, **kwargs):
        return self

    def distinct(self):
        seen = []
        for row in self.rows:
            value = row if isinstance(row, str) else row.session_id
            if value not in seen:
                seen.append(value)
        return FakeQuery(seen)

    def order_by(self, *args, **kwargs):
        return FakeQuery(sorted(self.rows, key=lambda row: row.created_at, reverse=True))

    def limit(self, limit):
        return FakeQuery(self.rows[:limit])

    def all(self):
        return self.rows


class FakeDb:
    def __init__(self):
        self.rows = [
            ChatHistory(
                id=1,
                session_id="web-1",
                question="ORA-00942 table or view does not exist",
                answer="[오류 요약] table missing",
                created_at=datetime.utcnow(),
            ),
            ChatHistory(
                id=2,
                session_id="web-2",
                question="Git pull 오류",
                answer="[오류 요약] git pull failed",
                created_at=datetime.utcnow(),
            ),
        ]

    def query(self, model):
        if model is ChatHistory.session_id:
            return FakeQuery([row.session_id for row in self.rows])
        return FakeQuery(self.rows)


def override_get_db():
    yield FakeDb()


class WikiDashboardApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()

    def test_wiki_list_returns_documents_and_categories(self):
        response = self.client.get("/api/wiki")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data["count"], 0)
        self.assertIn("categories", data)
        self.assertIn("documents", data)

    def test_wiki_search_filters_by_keyword(self):
        response = self.client.get("/api/wiki/search", params={"keyword": "ORA-00942"})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(data["count"], 1)

    def test_wiki_detail_returns_single_document(self):
        document_id = wiki_service.list_documents()[0]["id"]
        response = self.client.get(f"/api/wiki/{document_id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], document_id)

    def test_dashboard_summary_uses_chat_history_and_wiki_count(self):
        response = self.client.get("/api/dashboard/summary")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_questions"], 2)
        self.assertEqual(data["active_users"], 2)
        self.assertGreater(data["wiki_documents"], 0)

    def test_dashboard_recent_logs_returns_required_columns(self):
        response = self.client.get("/api/dashboard/recent-logs")

        self.assertEqual(response.status_code, 200)
        first = response.json()[0]
        self.assertIn("time", first)
        self.assertIn("user", first)
        self.assertIn("question", first)
        self.assertIn("answer_summary", first)
        self.assertIn("category", first)
        self.assertIn("response_time", first)


if __name__ == "__main__":
    unittest.main()
