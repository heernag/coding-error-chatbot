import { FormEvent, useEffect, useMemo, useState } from "react";
import { fetchWikiDocuments, searchWikiDocuments, WikiDocument } from "../api";

const emptyDocuments: WikiDocument[] = [];

export function WikiSearchBar({ value, onChange, onSubmit }: { value: string; onChange: (value: string) => void; onSubmit: () => void }) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form className="wiki-search" onSubmit={handleSubmit}>
      <label htmlFor="wiki-keyword">오류 코드 또는 키워드</label>
      <div>
        <input
          id="wiki-keyword"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="ORA-00942, CORS, permission..."
        />
        <button type="submit">검색</button>
      </div>
    </form>
  );
}

export function WikiCategoryFilter({ categories, selected, onSelect }: { categories: string[]; selected: string; onSelect: (category: string) => void }) {
  return (
    <nav className="wiki-categories" aria-label="위키 카테고리">
      <button className={selected === "전체" ? "active" : ""} onClick={() => onSelect("전체")} type="button">
        전체
      </button>
      {categories.map((category) => (
        <button className={selected === category ? "active" : ""} key={category} onClick={() => onSelect(category)} type="button">
          {category}
        </button>
      ))}
    </nav>
  );
}

export function WikiList({ documents, selectedId, onSelect }: { documents: WikiDocument[]; selectedId?: string; onSelect: (document: WikiDocument) => void }) {
  return (
    <section className="wiki-list" aria-label="오류 문서 목록">
      {documents.map((document) => (
        <button
          className={`wiki-list-item ${selectedId === document.id ? "selected" : ""}`}
          key={document.id}
          onClick={() => onSelect(document)}
          type="button"
        >
          <span>{document.category}</span>
          <strong>{document.error_code}</strong>
          <small>{document.title}</small>
        </button>
      ))}
      {documents.length === 0 ? <p className="empty-state">검색된 위키 문서가 없습니다.</p> : null}
    </section>
  );
}

function TextList({ items }: { items: string[] }) {
  if (!items.length) {
    return <p>등록된 내용이 없습니다.</p>;
  }
  return (
    <ul>
      {items.map((item, index) => (
        <li key={`${item}-${index}`}>{item}</li>
      ))}
    </ul>
  );
}

export function WikiDetail({ document }: { document?: WikiDocument }) {
  if (!document) {
    return <aside className="wiki-detail empty-state">왼쪽 목록에서 오류 문서를 선택해 주세요.</aside>;
  }

  return (
    <aside className="wiki-detail">
      <div className="detail-heading">
        <span>{document.category}</span>
        <h2>{document.error_code}</h2>
        <p>{document.title}</p>
      </div>

      <section>
        <h3>설명</h3>
        <p>{document.description || document.error_message || "등록된 설명이 없습니다."}</p>
      </section>
      <section>
        <h3>원인</h3>
        <TextList items={document.cause} />
      </section>
      <section>
        <h3>진단 방법</h3>
        <TextList items={document.diagnosis} />
      </section>
      <section>
        <h3>해결 방법</h3>
        <TextList items={document.solution} />
      </section>
      <section>
        <h3>예제 코드 또는 명령어</h3>
        <pre>{document.examples.length ? document.examples.join("\n") : "등록된 예제가 없습니다."}</pre>
      </section>
      <section>
        <h3>관련 키워드</h3>
        <div className="keyword-chips">
          {document.keywords.map((keyword) => (
            <span key={keyword}>{keyword}</span>
          ))}
        </div>
      </section>
    </aside>
  );
}

export function WikiPage() {
  const [documents, setDocuments] = useState<WikiDocument[]>(emptyDocuments);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("전체");
  const [selectedDocument, setSelectedDocument] = useState<WikiDocument | undefined>();
  const [keyword, setKeyword] = useState("");
  const [status, setStatus] = useState("위키 문서를 불러오는 중입니다.");

  useEffect(() => {
    fetchWikiDocuments()
      .then((data) => {
        setDocuments(data.documents);
        setCategories(data.categories);
        setSelectedDocument(data.documents[0]);
        setStatus("");
      })
      .catch(() => {
        setStatus("백엔드 위키 API 연결을 확인해 주세요.");
      });
  }, []);

  const filteredDocuments = useMemo(() => {
    if (selectedCategory === "전체") {
      return documents;
    }
    return documents.filter((document) => document.category === selectedCategory);
  }, [documents, selectedCategory]);

  function runSearch() {
    searchWikiDocuments(keyword)
      .then((data) => {
        setDocuments(data.documents);
        setSelectedCategory("전체");
        setSelectedDocument(data.documents[0]);
        setStatus(data.documents.length ? "" : "검색 결과가 없습니다.");
      })
      .catch(() => setStatus("검색 API 연결을 확인해 주세요."));
  }

  return (
    <main className="page-shell wiki-page">
      <header className="page-title">
        <div>
          <span>IT Error Wiki</span>
          <h1>IT 오류 위키</h1>
        </div>
        <p>RAG에 사용 중인 오류 문서를 검색하고 상세 내용을 확인합니다.</p>
      </header>

      <div className="wiki-layout">
        <aside className="wiki-sidebar">
          <WikiSearchBar value={keyword} onChange={setKeyword} onSubmit={runSearch} />
          <WikiCategoryFilter categories={categories} selected={selectedCategory} onSelect={setSelectedCategory} />
        </aside>
        <WikiList documents={filteredDocuments} selectedId={selectedDocument?.id} onSelect={setSelectedDocument} />
        <WikiDetail document={selectedDocument} />
      </div>
      {status ? <p className="notice-text">{status}</p> : null}
    </main>
  );
}

