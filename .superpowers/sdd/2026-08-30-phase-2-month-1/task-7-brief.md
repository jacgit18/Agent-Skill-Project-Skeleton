# Task 7: Authentication Routes (Register, Login)

**Files:**
- Create: `app/routes/auth.py`
- Create: `app/routes/__init__.py`

**Interfaces:**
- Consumes: User model, UserCreate/UserResponse schemas, auth utilities
- Produces:
  - `POST /api/auth/register` → UserResponse
  - `POST /api/auth/login` → Token
  - `POST /api/auth/logout` (placeholder)

## Steps

### Step 1: Create app/routes/__init__.py

```python
# Routes package
```

### Step 2: Create app/routes/auth.py

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.expense import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token
from app.utils.auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    """Login and get access token."""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    """Logout (stateless—token simply expires)."""
    return {"message": "Logout successful"}
```

### Step 3: Commit

```bash
git add app/routes/auth.py app/routes/__init__.py
git commit -m "feat: add authentication endpoints (register, login, logout)

Endpoints:
- POST /api/auth/register (create new user)
- POST /api/auth/login (get JWT token)
- POST /api/auth/logout (stateless logout)

Features:
- Email/username uniqueness validation
- Bcrypt password hashing
- JWT token generation (30-min expiry)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

Task 7 creates auth routes. It depends on models (Task 2), schemas (Task 4), and auth utilities (Task 5). Task 6 imports these routes.

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
