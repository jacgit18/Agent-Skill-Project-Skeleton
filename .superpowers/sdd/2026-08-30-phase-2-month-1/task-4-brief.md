# Task 4: Pydantic Schemas (Request/Response)

**Files:**
- Create: `app/schemas/__init__.py`
- Create: `app/schemas/user.py`
- Create: `app/schemas/expense.py`
- Create: `app/schemas/auth.py`

**Interfaces:**
- Consumes: User, Expense, Category, Insight ORM models
- Produces:
  - User schemas: UserCreate, UserResponse
  - Expense schemas: ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseWithCategory
  - Category schemas: CategoryCreate, CategoryResponse
  - Auth schemas: Token, TokenData

## Steps

### Step 1: Create app/schemas/__init__.py

```python
from app.schemas.user import UserCreate, UserResponse
from app.schemas.expense import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseWithCategory,
    CategoryCreate, CategoryResponse
)
from app.schemas.auth import Token, TokenData

__all__ = [
    "UserCreate", "UserResponse",
    "ExpenseCreate", "ExpenseUpdate", "ExpenseResponse", "ExpenseWithCategory",
    "CategoryCreate", "CategoryResponse",
    "Token", "TokenData",
]
```

### Step 2: Create app/schemas/user.py

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### Step 3: Create app/schemas/expense.py

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    color: str = "#808080"

class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    category_id: Optional[int] = None
    date: Optional[datetime] = None

class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    date: Optional[datetime] = None

class ExpenseResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    description: str
    date: datetime
    created_at: datetime
    category_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class ExpenseWithCategory(ExpenseResponse):
    category: Optional[CategoryResponse] = None
```

### Step 4: Create app/schemas/auth.py

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
```

### Step 5: Commit

```bash
git add app/schemas/
git commit -m "feat: add Pydantic schemas for request/response validation

Schemas:
- User: Create, Response
- Expense: Create, Update, Response, WithCategory
- Category: Create, Response
- Auth: Token, TokenData

All schemas use from_attributes=True for ORM compatibility

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

Task 4 creates Pydantic schemas used for validation and serialization. These schemas use the ORM models created in Task 2 with `from_attributes=True` to allow conversion between ORM and Pydantic models.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
