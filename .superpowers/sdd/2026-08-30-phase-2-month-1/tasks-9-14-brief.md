# Tasks 9-14: Testing & Documentation

These final tasks focus on test setup, test implementation, and documentation. They consume output from Tasks 1-8.

---

## Task 9: Testing Setup & Fixtures

**Files:**
- Create: `tests/conftest.py`

**Interfaces:**
- Produces: pytest fixtures for database, client, test user, and auth token

Use the exact code from the plan's Task 9 section.

Commit message:
```
git commit -m "test: add pytest fixtures for database and test client

Fixtures:
- test_db: in-memory SQLite with table creation
- db_session: transactional database session
- client: FastAPI TestClient with mocked DB
- test_user: sample user for testing
- test_user_token: JWT token for auth tests

Supports isolated test runs with automatic cleanup

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 10: Unit Tests for Models

**Files:**
- Create: `tests/test_models.py`

**Interfaces:**
- Consumes: ORM models, fixtures from conftest
- Produces: Tests verifying model creation, relationships, constraints

Use the exact code from the plan's Task 10 section.

After implementing, run:
```bash
pytest tests/test_models.py -v
```

Commit message:
```
git commit -m "test: add unit tests for ORM models

Tests:
- User creation and uniqueness constraints
- Category creation
- Expense creation with relationships
- User → Expenses relationship (cascade)
- Category → Expenses relationship

Verifies data integrity and ORM correctness

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 11: Integration Tests for Auth Routes

**Files:**
- Create: `tests/test_auth.py`

**Interfaces:**
- Consumes: FastAPI test client, fixtures, auth schemas
- Produces: Tests for register/login/logout endpoints

Use the exact code from the plan's Task 11 section.

After implementing, run:
```bash
pytest tests/test_auth.py -v
```

Commit message:
```
git commit -m "test: add integration tests for authentication routes

Tests:
- Register: success, duplicate email, duplicate username
- Login: success, invalid email, invalid password
- Logout: success

Covers auth flow and error cases

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 12: Integration Tests for Expense Routes

**Files:**
- Create: `tests/test_expenses.py`

**Interfaces:**
- Consumes: FastAPI test client, fixtures, expense schemas
- Produces: Tests for CRUD endpoints, user isolation, authorization

Use the exact code from the plan's Task 12 section.

After implementing, run:
```bash
pytest tests/test_expenses.py -v
```

Commit message:
```
git commit -m "test: add integration tests for expense CRUD endpoints

Tests:
- Category: list, create, duplicate prevention
- Expense: create, list, get, update, delete
- User isolation (cannot see other users' expenses)
- Authorization (requires token)

Comprehensive coverage of CRUD operations and security

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 13: README Documentation

**Files:**
- Create: `README.md`
- Create: `docs/architecture.md`
- Create: `docs/setup.md`

**Interfaces:**
- Produces: Clear setup and usage documentation

Use the exact code from the plan's Task 13 section for all three files.

Commit message:
```
git commit -m "docs: add comprehensive setup and architecture documentation

Includes:
- README with quick start and endpoint list
- Architecture: schema design, integration points for AI
- Setup: step-by-step development environment guide

Covers: prerequisites, installation, testing, debugging, troubleshooting

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Task 14: Verify All Tests Pass & Final Cleanup

**Interfaces:**
- Consumes: All previous tasks
- Produces: Green test suite, clean git history

### Steps:

1. Run full test suite:
```bash
pytest -v --cov=app
```
Expected: All tests pass with good coverage.

2. Verify app starts:
```bash
python main.py
```
Let it run for 10 seconds, then Ctrl+C to stop.

3. Final commit (after all tests pass):
```bash
git add -A
git commit -m "Month 1: Financial Dashboard Foundation complete

Deliverables:
- SQLAlchemy ORM models (User, Expense, Category, Insight)
- FastAPI CRUD endpoints with JWT auth
- Comprehensive test suite (models, routes, auth)
- Environment configuration and documentation

Status: Ready for Month 2 (Console Chatbot integration)

All tests passing. API documented at /docs.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Implementation Notes

- Tasks 9-12 can be batched into one subagent dispatch if preferred (all tests together)
- Task 13 (docs) should be its own dispatch
- Task 14 (verification) is final and must have all tests passing
- Use exact code from plan; there are no code decisions to make for these tasks
