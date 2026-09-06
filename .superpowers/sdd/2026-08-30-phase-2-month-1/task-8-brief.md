# Task 8: Expense CRUD Routes

**Files:**
- Create: `app/routes/expenses.py`

**Interfaces:**
- Consumes: Expense, Category models; expense schemas; get_current_user dependency
- Produces:
  - `GET /api/expenses` → list[ExpenseWithCategory]
  - `POST /api/expenses` → ExpenseResponse
  - `GET /api/expenses/{id}` → ExpenseWithCategory
  - `PUT /api/expenses/{id}` → ExpenseWithCategory
  - `DELETE /api/expenses/{id}` → 204 No Content
  - `GET /api/categories` → list[CategoryResponse]
  - `POST /api/categories` → CategoryResponse

## Full Implementation

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.expense import User, Expense, Category
from app.schemas.expense import (
    ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseWithCategory,
    CategoryCreate, CategoryResponse
)
from app.utils.dependencies import get_current_user
from datetime import datetime

router = APIRouter()

# Category endpoints

@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """Get all expense categories."""
    categories = db.query(Category).all()
    return categories

@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new expense category."""
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )
    
    new_category = Category(name=category_data.name, color=category_data.color)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Expense endpoints

@router.get("", response_model=list[ExpenseWithCategory])
def list_expenses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all expenses for current user."""
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).all()
    return expenses

@router.post("", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new expense for current user."""
    new_expense = Expense(
        user_id=current_user.id,
        amount=expense_data.amount,
        description=expense_data.description,
        category_id=expense_data.category_id,
        date=expense_data.date or datetime.utcnow()
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/{expense_id}", response_model=ExpenseWithCategory)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific expense."""
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    return expense

@router.put("/{expense_id}", response_model=ExpenseWithCategory)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an expense."""
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    update_data = expense_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)
    
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an expense."""
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found"
        )
    
    db.delete(expense)
    db.commit()
```

## Steps

### Step 1: Create app/routes/expenses.py

Copy the full implementation above into the file.

### Step 2: Commit

```bash
git add app/routes/expenses.py
git commit -m "feat: add expense CRUD endpoints with authentication

Endpoints:
- GET /api/expenses (list user's expenses)
- POST /api/expenses (create new expense)
- GET /api/expenses/{id} (get specific expense)
- PUT /api/expenses/{id} (update expense)
- DELETE /api/expenses/{id} (delete expense)
- GET /api/expenses/categories (list categories)
- POST /api/expenses/categories (create category)

Features:
- User isolation (only see own expenses)
- Timestamp management (created_at, date)
- Category association
- Full error handling

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

Task 8 creates expense CRUD routes. It depends on models (Task 2), schemas (Task 4), utilities (Task 5), and auth (Task 7). Task 6 imports these routes.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
