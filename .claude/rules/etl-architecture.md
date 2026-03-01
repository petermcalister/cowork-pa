---
paths: "**/extract/**/*.py, **/core/**/*.py, **/entity/**/*.py"
---

# ETL / Layered Architecture

**Purpose:** Layer responsibilities, import rules, and data flow patterns for projects with extract-transform-load or layered processing.

---

## Layer Diagram

```
┌─────────────────────────────────────────────────┐
│  EXTRACT Layer                                   │
│  Reads external data (files, APIs, streams)      │
│  Output: raw dicts or DataFrames                 │
├─────────────────────────────────────────────────┤
│  CORE Layer (Business Logic)                     │
│  Transforms, validates, enriches data            │
│  Orchestrates multi-step workflows               │
├─────────────────────────────────────────────────┤
│  ENTITY Layer (Data Models + Persistence)        │
│  Pydantic models, repository classes             │
│  Database read/write operations                  │
├─────────────────────────────────────────────────┤
│  UTILS Layer (Cross-cutting)                     │
│  Logging, config, common helpers                 │
│  Available to all layers                         │
└─────────────────────────────────────────────────┘
```

---

## Import Rules

| From \ To | Extract | Core | Entity | Utils |
|-----------|---------|------|--------|-------|
| **Extract** | - | NO | NO | YES |
| **Core** | YES | - | YES | YES |
| **Entity** | NO | NO | - | YES |
| **Utils** | NO | NO | NO | - |

**Key rule:** Extract produces raw data. Core consumes it and writes through Entity. Entity never imports from Extract or Core.

---

## Data Flow Pattern

```python
# extract/source_reader.py — Reads raw data
class SourceReader:
    def read(self, path: str) -> list[dict]:
        """Read source data, return raw dicts."""
        ...

# core/processor.py — Business logic
class DataProcessor:
    def __init__(self, schema: str):
        self.repo = EntityRepository(db, schema=schema)

    def process(self, raw_records: list[dict]) -> int:
        """Validate, transform, and persist records."""
        entities = [self._transform(r) for r in raw_records]
        return self.repo.batch_insert(entities)

    def _transform(self, raw: dict) -> EntityData:
        """Transform raw dict to entity model."""
        ...

# entity/models.py — Data models
class EntityData(BaseModel):
    ...

# entity/repository.py — Persistence
class EntityRepository:
    ...
```

---

## Orchestration Pattern

```python
# core/pipeline.py
class Pipeline:
    """Orchestrates a full ETL run."""

    def run(self, source_path: str, schema: str) -> dict:
        # Extract
        reader = SourceReader()
        raw_data = reader.read(source_path)

        # Transform + Load
        processor = DataProcessor(schema=schema)
        count = processor.process(raw_data)

        return {"records_processed": count, "status": "completed"}
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Entity imports from Extract | Add Core layer between them |
| Business logic in Extract | Extract only reads; Core transforms |
| Skipping validation | Validate in Core before Entity persistence |
| No schema parameter | Always pass schema through the pipeline |
| Monolithic processor | Break into Extract → Core → Entity steps |
