# Task 5: Authentication Utilities (Hashing & JWT)

**Files:**
- Create: `app/utils/auth.py`
- Create: `app/utils/__init__.py`
- Create: `app/utils/dependencies.py`

**Interfaces:**
- Consumes: passlib, python-jose, config
- Produces:
  - `hash_password(password: str) → str`
  - `verify_password(password: str, hash: str) → bool`
  - `create_access_token(data: dict, expires_delta: timedelta) → str`
  - `verify_token(token: str) → TokenData`
  - `get_current_user(token: str, db: Session) → User` (dependency)

## Steps

### Step 1: Create app/utils/__init__.py

```python
from app.utils.auth import hash_password, verify_password, create_access_token, verify_token
from app.utils.dependencies import get_current_user

__all__ = ["hash_password", "verify_password", "create_access_token", "verify_token", "get_current_user"]
```

### Step 2: Create app/utils/auth.py

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import get_settings
from app.schemas.auth import TokenData

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify JWT token and extract claims."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        if user_id is None:
            raise JWTError("Invalid token")
        return TokenData(user_id=user_id, email=email)
    except JWTError:
        raise JWTError("Invalid token")
```

### Step 3: Create app/utils/dependencies.py

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.utils.auth import verify_token
from app.database import get_db
from app.models.expense import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    try:
        token_data = verify_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user
```

### Step 4: Commit

```bash
git add app/utils/
git commit -m "feat: add authentication utilities (password hashing, JWT)

Functions:
- hash_password/verify_password (bcrypt)
- create_access_token (JWT with expiry)
- verify_token (JWT verification)
- get_current_user (FastAPI dependency for auth)

HTTPBearer security scheme for protected endpoints

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Context

Task 5 creates the authentication utilities used by routes in Task 7. It depends on config (Task 3) and schemas (Task 4).

**Working directory:** `/home/jac/AI/Agents/PromptingAgent/projects/financial-dashboard/backend`
