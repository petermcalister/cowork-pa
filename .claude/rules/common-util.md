---
paths: "**/*.py"
---

# Common Utility Instructions

---

## Configuration Constants

```python
from pathlib import Path

# Core paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "files"
OUTPUT_DIR = BASE_DIR / "files" / "output"
TEMP_DIR = BASE_DIR / "files" / "temp"
LOG_DIR = BASE_DIR / "logs"

# Database paths
DATABASE_DIR = DATA_DIR
```

---

## Environment Setup

```python
def load_environment_config(env: str = "dev") -> dict:
    """
    Load configuration specific to environment.

    Args:
        env: Environment name (dev, test, prod)

    Returns:
        Configuration dictionary
    """
    config_path = BASE_DIR / f"config_{env}.json"
    with open(config_path, 'r') as f:
        return json.load(f)
```

---

## Logger Configuration

```python
log_file = LOG_DIR / "application.log"
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def getLogger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
```

---

## Standard Exception Block

Use this exception handling pattern in ALL functions:

```python
import inspect
import logging

logger = getLogger(__name__)

def example_function():
    """Example function with standard exception handling."""
    try:
        # Function logic here
        pass
    except Exception as e:
        current_function = inspect.currentframe().f_code.co_name
        print(f"An error occurred in {current_function}: {e}")
        logger.warning(f"An error occurred in {current_function}: {e}")
        raise e
```

---

## Filepath Building Helper

```python
def safe_path(*parts) -> Path:
    """
    Build a safe file path from parts.

    Args:
        *parts: Path components

    Returns:
        Resolved Path object
    """
    return Path(*parts).resolve()
```

---

## Date/Time Utilities

```python
from datetime import datetime, timedelta

def get_current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, fmt)

def to_unix_timestamp(dt: datetime) -> int:
    """Convert datetime to Unix timestamp."""
    return int(dt.timestamp())

def from_unix_timestamp(ts: int) -> datetime:
    """Convert Unix timestamp to datetime."""
    return datetime.fromtimestamp(ts)
```

---

## Type Conversion Utilities

```python
def safe_int(value, default: int = 0) -> int:
    """Safely convert value to int with default."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default: float = 0.0) -> float:
    """Safely convert value to float with default."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_str(value, default: str = "") -> str:
    """Safely convert value to string with default."""
    if value is None:
        return default
    return str(value)
```

---

## List/Dict Transformation

```python
def rows_to_dicts(rows: list, columns: list[str]) -> list[dict]:
    """
    Convert database rows to list of dictionaries.

    Args:
        rows: List of tuples from database query
        columns: Column names in order

    Returns:
        List of dictionaries with column names as keys
    """
    return [dict(zip(columns, row)) for row in rows]
```

---

## File Operations

```python
def ensure_directory(path: Path) -> Path:
    """Ensure directory exists, create if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path

def read_json_file(filepath: Path) -> dict:
    """Read and parse JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(filepath: Path, data: dict) -> None:
    """Write data to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
```

---

## SQL Query Helpers

```python
def build_in_clause(values: list) -> str:
    """
    Build SQL IN clause from list of values.

    Args:
        values: List of values for IN clause

    Returns:
        Formatted IN clause string
    """
    if not values:
        return "(NULL)"

    if isinstance(values[0], str):
        formatted = ", ".join(f"'{v}'" for v in values)
    else:
        formatted = ", ".join(str(v) for v in values)

    return f"({formatted})"
```

---

## Validation Utilities

```python
def validate_required_fields(data: dict, required: list[str]) -> tuple[bool, list[str]]:
    """
    Validate that required fields are present in data.

    Returns:
        Tuple of (is_valid, missing_fields)
    """
    missing = [f for f in required if f not in data or data[f] is None]
    return len(missing) == 0, missing

def validate_type(value, expected_type: type, field_name: str) -> None:
    """Validate value is of expected type. Raises TypeError if not."""
    if not isinstance(value, expected_type):
        raise TypeError(f"{field_name} must be {expected_type.__name__}")
```

---

## Numeric Utilities

```python
def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator

def round_to_precision(value: float, precision: int = 2) -> float:
    """Round value to specified decimal precision."""
    return round(value, precision)
```

---

## Batch Processing

```python
def chunk_list(lst: list, chunk_size: int) -> list[list]:
    """Split list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
```

---

## Error Classes

```python
class DataValidationError(Exception):
    """Raised when data validation fails."""
    pass

class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""
    pass

class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass
```

---

## Quick Reference

| Category | Function | Purpose |
|----------|----------|---------|
| Logging | `getLogger()` | Standardized logging |
| Paths | `safe_path()` | Safe path construction |
| Data | `rows_to_dicts()` | DB result transformation |
| Validation | `validate_required_fields()` | Input validation |
| SQL | `build_in_clause()` | Query building |
| Batch | `chunk_list()` | Batch processing |
