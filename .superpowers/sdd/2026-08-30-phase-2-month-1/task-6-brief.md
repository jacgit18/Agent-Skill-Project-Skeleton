# Task 6: FastAPI App Setup & Middleware

**Files:**
- Create: `app/main.py`
- Create: `app/middleware/cors.py`
- Create: `app/middleware/__init__.py`

**Interfaces:**
- Consumes: FastAPI, SQLAlchemy, models, routes (to be created)
- Produces: 
  - `app` (FastAPI instance with CORS, startup events)
  - Database tables created on startup

## Steps

### Step 1: Create app/middleware/__init__.py

```python
# Middleware package
```

### Step 2: Create app/middleware/cors.py

```python
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """Add CORS middleware to FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Update for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
```

### Step 3: Create app/main.py

```python
from fastapi import FastAPI
from app.database import Base, engine
from app.middleware.cors import add_cors_middleware
from app.routes import auth, expenses

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Dashboard API",
    description="AI-powered personal finance dashboard",
    version="0.1.0",
)

# Add middleware
app = add_cors_middleware(app)

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])

@app.on_event("startup")
async def startup_event():
    print("Financial Dashboard API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Financial Dashboard API shutting down...")
```

### Step 4: Commit

```bash
git add app/main.py app/middleware/
git commit -m "feat: add FastAPI app initialization and CORS middleware

Setup:
- Create database tables on startup
- CORS middleware (allow localhost:3000, :8080)
- Health check endpoint
- Startup/shutdown event logging

Routes (to be included):
- auth: login, register, logout
- expenses: CRUD operations

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

Task 6 creates the main FastAPI app. It imports routes from `app.routes` (Tasks 7-8), which don't exist yet. The import will fail until those tasks complete. This is expected — routes are optional at startup.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
**Note:** Routes will be created in Tasks 7-8. For now, you can comment them out if needed, but the final version needs them included.
