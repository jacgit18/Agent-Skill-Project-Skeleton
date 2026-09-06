# Task 3: Configuration & Environment Setup

**Files:**
- Create: `app/config.py`

**Interfaces:**
- Consumes: .env file
- Produces: 
  - `get_settings()` → Settings object with database_url, secret_key, algorithm, debug flag

## Steps

### Step 1: Create app/config.py

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    database_url_test: str = "sqlite:///./test.db"
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    debug: bool = False
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

### Step 2: Commit

```bash
git add app/config.py
git commit -m "feat: add Pydantic settings for configuration management

Config options:
- database_url (PostgreSQL or SQLite)
- secret_key, algorithm (JWT auth)
- access_token_expire_minutes
- debug flag

Loaded from .env file via Pydantic BaseSettings

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

This task creates the configuration module that is imported by `app/database.py` (created in Task 2). Task 2's imports will now resolve correctly after this task completes.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
