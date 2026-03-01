---
paths: "**/entity/**/*.py, **/models/**/*.py"
---

# Entity Model Patterns

**Purpose:** Conventions for creating entity/model classes with Pydantic and repository patterns.

---

## Entity Structure

### Data Class (Pydantic Model)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class EntityData(BaseModel):
    """Immutable data representation of an entity."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    status: str = "active"
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"from_attributes": True}
```

### Repository Class

```python
class EntityRepository:
    """Handles persistence for Entity records."""

    def __init__(self, db, schema: Optional[str] = None):
        self.db = db
        self.schema = schema or get_default_schema()

    def insert(self, data: EntityData) -> UUID:
        """Insert a new entity record."""
        ...

    def get_by_id(self, entity_id: UUID) -> Optional[EntityData]:
        """Retrieve entity by primary key."""
        ...

    def find_by(self, **filters) -> list[EntityData]:
        """Query entities by filter criteria."""
        ...

    def update(self, entity_id: UUID, **fields) -> bool:
        """Update specific fields on an entity."""
        ...

    def delete(self, entity_id: UUID) -> bool:
        """Delete an entity by ID."""
        ...
```

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Data class | `{Name}Data` | `TaskData`, `UserData` |
| Repository | `{Name}Repository` | `TaskRepository` |
| DTO (if needed) | `{Name}Dto` | `TaskDto` |
| Table name | `snake_case`, plural | `tasks`, `user_profiles` |

---

## SCD Type 2 Pattern (Versioned Records)

For entities that need history tracking:

```python
class VersionedEntityData(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    entity_id: UUID  # Logical ID (same across versions)
    effective_from: datetime
    effective_to: Optional[datetime] = None  # NULL = current
    is_current: bool = True
    # ... business fields
```

---

## Batch SQL Generation

When inserting multiple records, build batch SQL:

```python
def batch_insert(self, records: list[EntityData]) -> int:
    """Insert multiple records in a single transaction."""
    if not records:
        return 0
    values_clauses = []
    params = []
    for record in records:
        values_clauses.append("(%s, %s, %s)")
        params.extend([record.id, record.name, record.status])
    sql = f"INSERT INTO {self.schema}.entities (id, name, status) VALUES {', '.join(values_clauses)}"
    return self.db.execute(sql, params)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Mutable default for `metadata` | Use `Field(default_factory=dict)` |
| Missing `model_config` | Add `{"from_attributes": True}` for ORM compat |
| Repository without schema param | Always accept optional schema override |
| No `updated_at` on updates | Set `updated_at = datetime.utcnow()` in update methods |
