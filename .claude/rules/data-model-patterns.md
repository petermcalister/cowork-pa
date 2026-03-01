---
paths: "**/entity/**/*.py, **/migrations/**/*.sql"
---

# Data Model Patterns Guide

**Purpose:** Data modeling concepts, table design principles, and entity patterns for this project.

---

## Table Design Principles

### Primary Keys

**Use UUID for all tables:**
```sql
CREATE TABLE {schema}.entity_name (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ...
);
```

**Why UUID:**
- No sequence coordination across environments
- Safe for distributed systems
- Merge-friendly across databases

### Required Columns

Every table should include:

| Column | Type | Purpose |
|--------|------|---------|
| `id` | UUID | Primary key |
| `created_at` | TIMESTAMPTZ | Record creation timestamp |
| `updated_at` | TIMESTAMPTZ | Last modification timestamp |

**For SCD tables, also include:**
- `effective_from` - Version start date
- `effective_to` - Version end date (NULL = current)
- `is_current` - Boolean flag for active version

---

## Entity Patterns

### Standard Entity

```sql
CREATE TABLE {schema}.entity_name (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Business columns
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',

    -- Audit columns
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

### Entity with Foreign Key

```sql
CREATE TABLE {schema}.child_entity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Foreign key reference
    parent_id UUID NOT NULL REFERENCES {schema}.parent_entity(id) ON DELETE CASCADE,

    -- Business columns
    attribute TEXT,

    -- Audit columns
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Index for FK lookups
CREATE INDEX idx_child_parent_id ON {schema}.child_entity(parent_id);
```

### Entity with JSONB Metadata

```sql
CREATE TABLE {schema}.flexible_entity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Structured columns
    entity_type VARCHAR(50) NOT NULL,

    -- Flexible metadata (JSONB)
    metadata JSONB DEFAULT '{}',

    -- Audit
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- GIN index for JSONB queries
CREATE INDEX idx_flexible_metadata ON {schema}.flexible_entity USING gin(metadata);
```

---

## Vector Embedding Tables

### Embedding Column Design

```sql
CREATE TABLE {schema}.embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Reference to source entity
    source_id UUID NOT NULL REFERENCES {schema}.source_entity(id),

    -- Vector embedding (768 dimensions for Google text-embedding-004)
    embedding vector(768),

    -- Embedding metadata
    model_name VARCHAR(100) DEFAULT 'text-embedding-004',
    chunk_index INTEGER DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

### Vector Index Options

**IVFFlat (faster builds, good for < 100K vectors):**
```sql
CREATE INDEX idx_embeddings_vector ON {schema}.embeddings
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

**HNSW (faster queries, better for production):**
```sql
CREATE INDEX idx_embeddings_vector ON {schema}.embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

---

## Naming Conventions

### Tables

- Use **snake_case** lowercase
- Use **plural** for collection tables: `emails`, `attachments`
- Use **singular** for join tables: `email_attachment`

### Columns

- Use **snake_case** lowercase
- Suffix foreign keys with `_id`: `email_id`, `user_id`
- Suffix dates with `_at` or `_date`: `created_at`, `sent_date`
- Suffix booleans with `is_` or `has_`: `is_active`, `has_attachment`

### Indexes

- Pattern: `idx_{table}_{column(s)}`
- Examples: `idx_emails_sender`, `idx_emails_sent_date`

### Constraints

- Primary key: `pk_{table}` or use default
- Foreign key: `fk_{table}_{referenced_table}`
- Unique: `uq_{table}_{column(s)}`
- Check: `chk_{table}_{description}`

---

## PostgreSQL Reserved Words

Quote these column names to avoid conflicts:

| Word | Issue | Solution |
|------|-------|----------|
| `user` | Reserved keyword | Use `"user"` or rename to `user_name` |
| `timestamp` | Type conflict | Use `"timestamp"` or rename to `event_time` |
| `offset` | Reserved keyword | Use `"offset"` or rename to `offset_value` |
| `order` | Reserved keyword | Use `"order"` or rename to `sort_order` |

