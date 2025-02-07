# Shared Ledger System

A monorepo-based **Shared Ledger System** designed to track user credits across multiple applications. 
This system ensures **type safety**, **code reuse**, and **extensibility** by allowing each application 
to add its own custom ledger operations on top of shared core operations.

---

## Table of Contents

1. [Project Purpose](#project-purpose)  
2. [Features](#features)  
3. [Technical Stack](#technical-stack)  
4. [Directory Structure](#directory-structure)  
5. [Core Concepts](#core-concepts)  
6. [Installation and Setup](#installation-and-setup)  
7. [Running the Applications](#running-the-applications)  
8. [API Endpoints](#api-endpoints)  
9. [Redoc Documentation](#redoc-documentation)  
10. [Testing](#testing)  
11. [Migration Examples](#migration-examples)  
12. [Submission Guidelines](#submission-guidelines)  
13. [Recommendations](#recommendations)  
14. [Contributing](#contributing)
15. [Acknowledgments](#acknowledgments)  
16. [License](#license)

---

## Project Purpose

- **Shared Ledger Logic**: Provide a single, core ledger implementation that all applications in the monorepo can leverage.
- **Type Safety**: Enforce a consistent, type-safe approach to shared ledger operations using Python Enums, Pydantic, and SQLAlchemy.
- **Extensibility**: Allow individual applications to define additional ledger operations without breaking shared functionality.
- **Database Integrity**: Ensure each transaction is tracked and stored with strict data integrity using Postgres and Alembic migrations.

---

## Features

- ✅ **Type-safe ledger operations**  
- ✅ **Enforced shared operations**  
- ✅ **Detailed logging**  
- ✅ **Async database operations with SQLAlchemy**  
- ✅ **Comprehensive test coverage**  
- ✅ **Alembic migrations**  

## Project Purpose

Design and implement a **Shared Ledger System** in a monorepo containing multiple applications.
Each application needs to track user credits through a ledger while enforcing shared operations,
type safety, and reusability.

### Background

- You are working on a monorepo where multiple applications all rely on a shared ledger functionality.
- Each application needs both the common ledger operations and potentially its own specialized operations.
- The core system must enforce mandatory operations (e.g., `DAILY_REWARD`, `SIGNUP_CREDIT`, `CREDIT_SPEND`, `CREDIT_ADD`)
  while allowing extension for app-specific needs.

> **Note**: Prometheus, Redis, rate limiting, or authentication are **not** implemented at this time.


---

## Technical Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy 2.0+**
- **Pydantic**
- **Alembic**
- **PostgreSQL**

### Example Ledger Configuration

```python
LEDGER_OPERATION_CONFIG = {
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}
```
---

## Directory Structure

A suggested directory layout for the monorepo is as follows:
```plaintext
shared-ledger-system/
      shared-ledger-system/
      ├── README.md
      ├── pyproject.toml
      ├── requirements.txt
      ├── .gitignore
      ├── .env
      ├── core/
      │   ├── init.py
      │   ├── ledgers/
      │   │   ├── init.py
      │   │   ├── models.py
      │   │   ├── schemas.py
      │   │   ├── operations.py
      │   │   ├── exceptions.py
      │   │   └── service.py
      │   └── db/
      │        ├── migrations/
      │        │     ├── alembic/
      │        │     │   ├── env.py
      │        │     │   └── versions/
      │        │     └── alembic.ini
      │        ├── init.py
      │        └── base.py
      ├── apps/
      │   ├── app1/
      │   │   ├── src/
      │   │   │   ├── init.py
      │   │   │   ├── api/
      │   │   │   │     └── core/
      │   │   │   │          ├── init.py
      │   │   │   │          └── ledgers/
      │   │   │   │                ├── init.py
      │   │   │   │                ├── routes.py
      │   │   │   │                └── schemas.py
      │   │   │   ├── init.py
      │   │   │   └── main.py
      │   │   └── tests/
      │   └── app2/
      │       └── (similar structure)
      └── tests/
              └── core/
              |  |── ledgers/
              |  |       ├── test_operations.py
              |  |       └── test_service.py
              |  └── conftest.py
              └── apps/
                  └── app1/
                        └── test_api.py

```

- **shared-ledger-system/:** The root directory of the monorepo.

    - README.md: Project description and instructions.
    - pyproject.toml: Project configuration file.
    - requirements.txt: List of dependencies.
    - .gitignore: Git ignore file.
    - .env: Environment variables file.

- **core/:** Houses the core ledger functionality.

- **core/ledgers/**: Shared ledger models, schemas, and operations.

- **apps/app1/**: A sample application demonstrating usage of the core ledger.

- **tests/**: Houses tests for both core and applications.

---

## Core Concepts

### Shared vs. Application-Specific Ledger Operations

- **Shared Operations**: `DAILY_REWARD`, `SIGNUP_CREDIT`, `CREDIT_SPEND`, `CREDIT_ADD`

- **App-Specific Operations**: For instance, `CONTENT_CREATION`, `CONTENT_ACCESS`

### Example Enum Usage

```python
# This should fail
class BadOperation(BaseLedgerOperation):
    CONTENT_CREATION = "CONTENT_CREATION"  # Missing shared operations!

# This should work
class GoodOperation(BaseLedgerOperation):
    # Required shared operations
    DAILY_REWARD = "DAILY_REWARD"
    SIGNUP_CREDIT = "SIGNUP_CREDIT"
    CREDIT_SPEND = "CREDIT_SPEND"
    CREDIT_ADD = "CREDIT_ADD"

    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
```

## Installation and Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd shared-ledger-system 
```
2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Set up environment variables (.env):
```env
DATABASE_URL=postgresql+asyncpg://postgres:12345@localhost:5432/shared_ledger_system
TEST_DATABASE_URL=postgresql+asyncpg://postgres:12345@localhost:5432/test_db
```
5. Run database migrations:
```
cd shared-ledger-system
cd core/db/migrations
alembic init alembic
alembic upgrade head
```
6. **Configure Application**:

   Adjust settings or config files as needed for each app.


## Running the Applications


1. Start PostgreSQL server
2. Run the application:

```bash
cd shared-ledger-system
uvicorn apps.app1.src.main:app --reload --host 0.0.0.0 --port 8000  
```

The API will be available at http://localhost:8000 
Swagger documentation at http://localhost:8000/docs 
3. **Usage**:

   - Access your app at [http://localhost:8000](http://localhost:8000)

---

### Usage    

1. Create a new ledger entry:
```curl     
curl -X POST http://localhost:8000/ledger/ -H "Content-Type: application/json" -d '{"operation": "CREDIT_ADD", "amount": 10, "owner_id": "test_user", "nonce": "123e4567-e89b-12d3-a456-426655440000"}'
```

2. Get the current balance of a user:
```curl
curl -X GET http://localhost:8000/ledger/test_user
```    
---

## API Endpoints

### GET /ledger/{owner_id}

- **Description**: Returns current balance for `owner_id`.

### POST /ledger

- **Request Body** (example):

  ```json
  {
    "owner_id": "user123",
    "operation": "CREDIT_ADD",
    "amount": 10,
    "nonce": "unique-transaction-id"
  }
  ```

- **Behavior**:

  1. Ensures sufficient balance if the operation is negative.
  2. Prevents duplicate transactions using `nonce`.

---

## Redoc Documentation

FastAPI provides Redoc out of the box. Visit:

```
http://localhost:8000/redoc
```

---

## Testing

1. **Run Tests**:

   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```

2. **Directory**:

   - **core tests**: `tests/core/ledgers/`
   - **app tests**: `apps/<app_name>/tests/`

---

## Migration Examples

1. **Create a New Migration**:

   ```bash
   cd core/db/migrations
   alembic revision -m "Add ledger table"
   ```

2. **Apply Migrations**:

   ```bash
   alembic upgrade head
   ```

3. **App-Specific**:

   Each app can maintain separate migration scripts if needed.

4. **Real-World Example**:

```python
# shared-ledger-system/core/db/migrations/alembic/versions/a71452189a36_initial_migration.py
"""Initial migration

Revision ID: a71452189a36
Revises: 
Create Date: 2025-02-05 16:30:59.255828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a71452189a36'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ledger_entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('operation', sa.String(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('nonce', sa.String(), nullable=False),
    sa.Column('owner_id', sa.String(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nonce')
    )
    op.create_index('idx_nonce', 'ledger_entries', ['nonce'], unique=False)
    op.create_index('idx_owner_id', 'ledger_entries', ['owner_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_owner_id', table_name='ledger_entries')
    op.drop_index('idx_nonce', table_name='ledger_entries')
    op.drop_table('ledger_entries')
    # ### end Alembic commands ###

 ```

---

## Submission Guidelines

1. **Submit via GitHub repository**

2. **Include**:

   - Implementation
   - Tests
   - Documentation
   - Migration examples

3. **Commit History**:

   Demonstrate step-by-step development progress.

---

## Recommendations

- **Environment Management**:

  Use a virtual environment to isolate dependencies.

- **Dependency Management**:

  Employ a package manager (pip, poetry).

- **Code Formatting**:

  Use a formatter (e.g., Black) for consistent style.

- **Static Type Checking**:

  Use mypy or pyright to detect type errors.

- **Linting**:

  Use flake8 or pylint for code quality checks.         

## Contributing

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push your changes
5. Create a pull request    
6. Request a pull requirements    


## Acknowledgments  

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)

## License
This project is provided under the [MIT License](LICENSE), unless stated otherwise in your repository.
