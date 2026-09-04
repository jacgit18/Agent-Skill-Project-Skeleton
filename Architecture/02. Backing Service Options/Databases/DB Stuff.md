---
tags: 
author:
  - gitUserNamePlaceHolder
banner: "![[Banner.gif]]"
banner_x: 
banner_y: 
cssclasses:
  - dashboard
Comments: Placeholder comment any thing else you want to mention about the document.
Purpose: This documentation discusses
Status: 
Started: 
EditDate: 
Relates:
---
### Summary of the conversation

We discussed **how database schemas are defined in a codebase** and the different architectural approaches you can take.

#### 1. Three major approaches to schema ownership

**Database-first**

- The database/SQL is the source of truth.
    
- You define tables and constraints using SQL migrations.
    
- Application code defines models/interfaces that represent the database.
    
- Common when database integrity, complex SQL, or shared databases are important.
    

**Code-first**

- The schema is primarily defined in application code.
    
- ORMs are one implementation of this approach, but **code-first does not mean ORM**.
    
- Examples discussed:
    
    - ORMs: Prisma, TypeORM, Sequelize, Django ORM, Entity Framework
        
    - Schema/validation libraries: Zod, Yup, io-ts, JSON Schema
        
    - Query builders: Knex, Kysely, SQLAlchemy Core
        
    - Database-driven code generation: sqlc, pgtyped
        

**Contract-first**

- Neither the application nor database is the primary source of truth.
    
- Instead, you define a formal **contract** describing how systems communicate.
    
- Examples:
    
    - OpenAPI
        
    - GraphQL
        
    - Protobuf/gRPC
        
    - JSON Schema
        
- The database becomes an implementation detail behind the contract.
    

---

### 2. Interfaces aren't necessarily database schemas

We specifically discussed the difference between something like:

```ts
interface User {
  id: string;
  email: string;
  createdAt: Date;
}
```

and an actual database schema.

An interface primarily describes what application code **expects**.

It doesn't necessarily enforce things like:

- `NOT NULL`
    
- `UNIQUE`
    
- foreign keys
    
- database constraints
    
- referential integrity
    

So an interface can accurately describe a type while the actual database has different rules.

---

### 3. Contract-first goes beyond interfaces

The important conceptual shift was:

> **An interface describes data for your code; a contract describes an agreement between systems.**

For example, an OpenAPI contract could specify:

```yaml
User:
  type: object
  required:
    - id
    - email
  properties:
    id:
      type: string
      format: uuid
    email:
      type: string
      format: email
    createdAt:
      type: string
      format: date-time
```

From that contract you can potentially generate:

- TypeScript/Python types
    
- Request/response validation
    
- API documentation
    
- Client SDKs
    
- API clients
    

The database doesn't have to mirror the contract exactly.

For example:

```text
                    CONTRACT
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      Frontend      Backend      API Docs
                       │
                       ↓
                  Domain Model
                       │
                       ↓
                   Database
```

The backend can translate between its internal database representation and the public contract.

---

### 4. Why mapping is important

We discussed that contract-first often involves explicit transformations such as:

```python
def to_user_response(row):
    return {
        "id": row["id"],
        "email": row["email"],
        "createdAt": row["created_at"],
    }
```

That extra mapping isn't necessarily wasted code.

It gives you a boundary where you can control:

- Which database fields are exposed
    
- Naming differences
    
- Security
    
- Backward compatibility
    
- Data transformations
    
- API evolution
    

The key principle was:

> **Don't automatically assume your database representation should become your public API representation.**

---

### 5. The choice between the three

You initially leaned toward **contract-first**, and after examining the alternatives, the recommendation was:

> **If forced to choose one by default, contract-first is the most compelling architectural choice—but it isn't universally appropriate.**

The reasoning wasn't simply that contract-first is "more scalable."

Its major benefit is that it forces you to clearly define **system boundaries and agreements**.

However, it can be overkill for:

- Throwaway projects
    
- Small internal tools
    
- Solo applications
    
- Systems where the schema is changing constantly
    
- Projects still in the exploration/discovery phase
    

For those, an ORM or query builder can be much more practical.

---

### 6. The more nuanced recommendation

A practical development lifecycle could look like:

```text
Exploration
    ↓
ORM / Query Builder
    ↓
Domain becomes clearer
    ↓
Define stable API contract
    ↓
Contract becomes boundary
    ↓
Database becomes implementation detail
```

So you don't necessarily need to be **contract-first from line one**.

You can start quickly, discover the domain, and introduce a formal contract once the system's external boundary becomes important.

---

### 7. The biggest takeaway

The most important concept from the conversation is **source of truth**.

When designing a system, ask:

> **Where does the authoritative definition of this data live?**

It could be:

**Database-first**

```text
SQL → Application
```

**Code-first**

```text
Code/ORM → Database
```

**Contract-first**

```text
Contract → Systems
              ↓
        Application → Database
```

And importantly:

> **ORM, query builder, schema library, interface, migration, and API contract are not interchangeable concepts.**

They solve different problems and can be used together.

For the kinds of backend/full-stack systems you're likely to encounter, learning **contracts + validation + explicit domain/persistence separation**, while also being comfortable with SQL and an ORM/query builder, would give you a much stronger mental model than simply learning one ORM deeply.