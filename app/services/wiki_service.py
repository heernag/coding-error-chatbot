from functools import lru_cache
from pathlib import Path
import json


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "it_engineer_chatbot_150_fixed.json"


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return [str(value)] if value else []


def _as_text(value):
    return "\n".join(_as_list(value))


@lru_cache(maxsize=1)
def get_wiki_documents():
    with DATA_FILE.open("r", encoding="utf-8") as file:
        raw_items = json.load(file)

    documents = []
    for index, item in enumerate(raw_items, start=1):
        doc_id = str(item.get("id") or item.get("error_code") or index)
        keywords = _as_list(item.get("keywords"))
        examples = _as_list(item.get("command_example")) + _as_list(item.get("examples"))
        search_text = " ".join(
            [
                doc_id,
                item.get("category") or "",
                item.get("subcategory") or "",
                item.get("error_code") or "",
                item.get("title") or "",
                item.get("error_message") or "",
                item.get("description") or "",
                _as_text(item.get("cause")),
                _as_text(item.get("diagnosis")),
                _as_text(item.get("solution")),
                _as_text(item.get("keywords")),
            ]
        ).lower()

        documents.append(
            {
                "id": doc_id,
                "category": item.get("category") or "Uncategorized",
                "subcategory": item.get("subcategory") or "",
                "error_code": item.get("error_code") or doc_id,
                "title": item.get("title") or doc_id,
                "error_message": item.get("error_message") or "",
                "description": item.get("description") or "",
                "cause": _as_list(item.get("cause")),
                "diagnosis": _as_list(item.get("diagnosis")),
                "solution": _as_list(item.get("solution")),
                "examples": examples,
                "keywords": keywords,
                "caution": item.get("caution") or "",
                "source_title": item.get("source_title") or "",
                "source_url": item.get("source_url") or "",
                "updated_at": item.get("updated_at") or "",
                "search_text": search_text,
            }
        )
    return documents


def public_document(document):
    return {key: value for key, value in document.items() if key != "search_text"}


def list_documents():
    return [public_document(document) for document in get_wiki_documents()]


def list_categories():
    return sorted({document["category"] for document in get_wiki_documents()})


def search_documents(keyword: str):
    normalized = (keyword or "").strip().lower()
    if not normalized:
        return list_documents()
    return [
        public_document(document)
        for document in get_wiki_documents()
        if normalized in document["search_text"]
    ]


def documents_by_category(category: str):
    normalized = (category or "").strip().lower()
    return [
        public_document(document)
        for document in get_wiki_documents()
        if document["category"].lower() == normalized
    ]


def get_document(document_id: str):
    normalized = (document_id or "").strip().lower()
    for document in get_wiki_documents():
        if document["id"].lower() == normalized:
            return public_document(document)
    return None


def find_category_for_text(text: str):
    normalized = (text or "").lower()
    if not normalized:
        return "Unknown"

    for document in get_wiki_documents():
        error_code = document["error_code"].lower()
        if error_code and error_code in normalized:
            return document["category"]

    category_hits = {}
    for document in get_wiki_documents():
        score = 0
        for keyword in document["keywords"][:8]:
            if keyword and keyword.lower() in normalized:
                score += 1
        if document["category"].lower() in normalized:
            score += 2
        if score:
            category_hits[document["category"]] = category_hits.get(document["category"], 0) + score

    if category_hits:
        return max(category_hits.items(), key=lambda item: item[1])[0]
    return "Unknown"
