from fastapi import APIRouter, HTTPException, Query

from app.services import wiki_service


router = APIRouter()


@router.get("/wiki")
async def get_wiki():
    documents = wiki_service.list_documents()
    return {
        "count": len(documents),
        "categories": wiki_service.list_categories(),
        "documents": documents,
    }


@router.get("/wiki/search")
async def search_wiki(keyword: str = Query(default="")):
    documents = wiki_service.search_documents(keyword)
    return {
        "keyword": keyword,
        "count": len(documents),
        "documents": documents,
    }


@router.get("/wiki/category/{category}")
async def get_wiki_by_category(category: str):
    documents = wiki_service.documents_by_category(category)
    return {
        "category": category,
        "count": len(documents),
        "documents": documents,
    }


@router.get("/wiki/{document_id}")
async def get_wiki_document(document_id: str):
    document = wiki_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Wiki document not found")
    return document
