# Task 1: Project Setup & Dependencies

**Files:**
- Create: `projects/financial-dashboard/backend/requirements.txt`
- Create: `projects/financial-dashboard/backend/.env.example`
- Create: `projects/financial-dashboard/backend/.gitignore`
- Create: `projects/financial-dashboard/backend/main.py`
- Create: `projects/financial-dashboard/backend/app/__init__.py`

**Interfaces:**
- Produces: Python environment with all dependencies installed; entry point at `main.py`

## Steps

### Step 1: Create project directory structure

```bash
mkdir -p projects/financial-dashboard/backend/app/{models,schemas,routes,utils,middleware}
mkdir -p projects/financial-dashboard/backend/tests
mkdir -p projects/financial-dashboard/docs
cd projects/financial-dashboard/backend
```

### Step 2: Create requirements.txt with core dependencies

```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pydantic==2.5.0
pydantic-settings==2.1.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### Step 3: Create .env.example

```
DATABASE_URL=postgresql://user:password@localhost/financial_db
DATABASE_URL_TEST=sqlite:///./test.db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

### Step 4: Create .gitignore

```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
.env
.env.local
*.db
*.sqlite
*.sqlite3
.DS_Store
.idea/
.vscode/
*.log
```

### Step 5: Create empty app/__init__.py

```python
# Financial Dashboard Backend
```

### Step 6: Create main.py entry point (minimal)

```python
from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### Step 7: Set up virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 8: Create initial .env

```bash
cp .env.example .env
# Edit .env with your local database URL
```

### Step 9: Commit

```bash
git add requirements.txt .env.example .gitignore app/ main.py
git commit -m "init: financial dashboard backend project structure

Core dependencies: FastAPI, SQLAlchemy, Pydantic
Auth: passlib, python-jose
Testing: pytest, pytest-asyncio
Database: psycopg2 (PostgreSQL)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

This is Month 1 of an AI-powered learning portfolio. You're building the foundation for a financial dashboard that will integrate with Claude AI in subsequent months.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent`
**Current git branch:** main

The project structure follows FastAPI conventions with SQLAlchemy ORM. Months 2-9 will add chat, categorization, file I/O, and RAG features.
