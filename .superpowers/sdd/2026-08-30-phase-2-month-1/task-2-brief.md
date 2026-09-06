# Task 2: Database Models (User, Expense, Category, Insight)

**Files:**
- Create: `app/models/expense.py`
- Create: `app/models/__init__.py`
- Create: `app/database.py`

**Interfaces:**
- Consumes: SQLAlchemy 2.0
- Produces: 
  - `User` (id, email, username, password_hash, created_at, expenses)
  - `Expense` (id, user_id, amount, description, category_id, date, created_at)
  - `Category` (id, name, color, created_at)
  - `Insight` (id, user_id, type, text, created_at)

## Steps

### Step 1: Create app/database.py (SQLAlchemy session)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.database_url, echo=settings.debug)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Step 2: Create app/models/__init__.py

```python
from app.models.expense import User, Expense, Category, Insight

__all__ = ["User", "Expense", "Category", "Insight"]
```

### Step 3: Create app/models/expense.py (all ORM models)

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    insights = relationship("Insight", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String, default="#808080")  # hex color for UI
    created_at = Column(DateTime, default=datetime.utcnow)
    
    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    amount = Column(Float)
    description = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

class Insight(Base):
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # "trend", "anomaly", "suggestion", etc.
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="insights")
```

### Step 4: Commit

```bash
git add app/database.py app/models/
git commit -m "feat: add SQLAlchemy ORM models (User, Expense, Category, Insight)

Schema design:
- User: email, username, password_hash, timestamps
- Expense: amount, description, category (FK), date
- Category: name, color for UI
- Insight: type (trend/anomaly/suggestion), generated text

Relationships:
- User → many Expenses (cascade delete)
- User → many Insights (cascade delete)
- Category → many Expenses
- Expense → one Category

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

Task 1 completes project structure and dependencies. Task 2 builds on that by creating the SQLAlchemy ORM models. Task 3 will add configuration (which is imported by database.py), so complete Task 3 right after this one.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
**Note:** app/config.py doesn't exist yet (Task 3 creates it), but this task's database.py imports from it. The import will fail until Task 3 completes, which is expected — it's why these tasks are sequential.
