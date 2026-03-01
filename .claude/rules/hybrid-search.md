---
paths: "**/search/**/*.py, **/query/**/*.py"
---

# Hybrid Search Patterns

**Purpose:** Vector + keyword search patterns using PostgreSQL pgvector and BM25/full-text search with Reciprocal Rank Fusion.

---

## Architecture Overview

```
┌──────────────┐    ┌──────────────┐
│ Vector Search │    │ Keyword Search│
│ (pgvector)   │    │ (BM25/tsvec) │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └──────┬────────────┘
              │
       ┌──────▼───────┐
       │ RRF Fusion   │
       │ (rank merge) │
       └──────┬───────┘
              │
       ┌──────▼───────┐
       │ Final Results│
       └──────────────┘
```

---

## Vector Search (Semantic)

```sql
-- Table with embedding column
CREATE TABLE {schema}.documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    embedding vector(768),
    search_content TEXT,  -- Precomputed searchable text
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- HNSW index for fast similarity search
CREATE INDEX idx_documents_embedding ON {schema}.documents
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Similarity query
SELECT id, content, 1 - (embedding <=> $1::vector) AS similarity
FROM {schema}.documents
WHERE 1 - (embedding <=> $1::vector) > 0.3
ORDER BY embedding <=> $1::vector
LIMIT 20;
```

---

## Keyword Search (BM25 / Full-Text)

```sql
-- Add tsvector column and index
ALTER TABLE {schema}.documents
    ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(search_content, ''))) STORED;

CREATE INDEX idx_documents_search ON {schema}.documents USING gin(search_vector);

-- Full-text query with ranking
SELECT id, content, ts_rank(search_vector, query) AS rank
FROM {schema}.documents, plainto_tsquery('english', $1) query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

---

## Reciprocal Rank Fusion (RRF)

```python
def reciprocal_rank_fusion(
    vector_results: list[dict],
    keyword_results: list[dict],
    k: int = 60,
    vector_weight: float = 0.6,
    keyword_weight: float = 0.4,
) -> list[dict]:
    """Merge vector and keyword results using RRF."""
    scores = {}

    for rank, result in enumerate(vector_results):
        doc_id = result["id"]
        scores[doc_id] = scores.get(doc_id, {"score": 0, "data": result})
        scores[doc_id]["score"] += vector_weight / (k + rank + 1)

    for rank, result in enumerate(keyword_results):
        doc_id = result["id"]
        scores[doc_id] = scores.get(doc_id, {"score": 0, "data": result})
        scores[doc_id]["score"] += keyword_weight / (k + rank + 1)

    merged = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [item["data"] | {"rrf_score": item["score"]} for item in merged]
```

---

## Embedding Generation

```python
def generate_embedding(text: str, model: str = "text-embedding-004") -> list[float]:
    """Generate embedding vector for text content."""
    # Use your preferred embedding provider
    response = embedding_client.embed(text=text, model=model)
    return response.embedding
```

---

## Search Service Pattern

```python
class HybridSearchService:
    def __init__(self, db, schema: str):
        self.db = db
        self.schema = schema

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Execute hybrid search combining vector and keyword results."""
        query_embedding = generate_embedding(query)

        vector_results = self._vector_search(query_embedding, limit=limit * 2)
        keyword_results = self._keyword_search(query, limit=limit * 2)

        fused = reciprocal_rank_fusion(vector_results, keyword_results)
        return fused[:limit]
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing vector index | Create HNSW or IVFFlat index |
| Low similarity threshold | Start at 0.3, tune based on results |
| No `search_content` column | Precompute searchable text for BM25 |
| Equal RRF weights | Tune vector_weight vs keyword_weight for your data |
| Embedding dimension mismatch | Match vector column size to model output |
