---
paths: "**/layout/**/*.py, **/pages/**/*.py, **/app.py"
---

# Streamlit Development Patterns

**Purpose:** Streamlit-specific patterns, common pitfalls, and best practices.

---

## Critical: Use st.form() for Input + Button Combinations

**ANY input widget + button must be wrapped in `st.form()`.**

```python
# WRONG - Input value lost on button click
name = st.text_input("Name", key='name_input')
if st.button("Submit"):
    process(name)  # name is EMPTY here

# CORRECT - Form captures values atomically
with st.form(key='my_form'):
    name = st.text_input("Name", key='name_input')
    submitted = st.form_submit_button("Submit")

if submitted:
    process(name)  # name has correct value
```

**Place `if submitted:` handler OUTSIDE the `with st.form():` block.**

---

## Session State Management

```python
# Initialize at top of file, before any conditional logic
if 'schema' not in st.session_state:
    st.session_state.schema = get_default_schema()

if 'refresh_trigger' not in st.session_state:
    st.session_state.refresh_trigger = 0
```

### Refresh Pattern

```python
def trigger_refresh():
    st.session_state.refresh_trigger += 1

@st.cache_data(ttl=30)
def load_data(schema: str, refresh: int):
    return fetch_from_database(schema=schema)

# After data modification
trigger_refresh()
st.rerun()
```

**Do NOT use underscore prefix on `refresh` param** — that excludes it from the cache key.

---

## Page Configuration

`st.set_page_config()` must be the first Streamlit command in the file:

```python
import streamlit as st

st.set_page_config(page_title="App Title", page_icon="", layout="wide")

# Other imports after this
```

---

## Layout Patterns

### Columns with Buttons

```python
col1, col2, col3 = st.columns([4, 1, 1])
with col1:
    st.markdown(f"**{item_name}**")
with col2:
    st.write("")  # Spacer for vertical alignment
    if st.button("Edit", key=f'edit_{idx}'):
        handle_edit()
```

### Dynamic Keys in Loops

```python
for idx, item in enumerate(items):
    st.text_input("Name", key=f'name_{idx}')
    st.button("Save", key=f'save_{idx}')
```

---

## Database Operations

```python
db = DatabaseManager()

@st.cache_data(ttl=30)
def load_data(schema: str, refresh: int):
    return Entity.get_all(db, schema=schema)

if st.button("Save Changes"):
    try:
        with db.begin_transaction() as txn:
            Entity.update(db, data)
            txn.commit()
        st.success("Changes saved!")
        trigger_refresh()
        st.rerun()
    except Exception as e:
        st.error(f"Failed to save: {e}")
```

---

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Button loses input values | Not using `st.form()` | Wrap input + button in form |
| Stale cached data | Cache not invalidated | Use refresh trigger + `st.rerun()` |
| `DuplicateWidgetID` | Same key for multiple widgets | Include unique ID in key |
| `set_page_config()` error | Not first st.* call | Move to very top of file |
| Sidebar resets on action | Not stored in session_state | Use `st.session_state` |

---

## Quick Reference

| Pattern | Use When |
|---------|----------|
| `st.form()` | Any input + button combination |
| `st.session_state` | Persisting values across reruns |
| `@st.cache_data` | Expensive data fetches |
| `_param` prefix | Unhashable cache parameters only |
| `trigger_refresh()` | After data modifications |
| `st.rerun()` | Force page refresh after state change |
