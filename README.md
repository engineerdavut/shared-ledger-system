                              
---

# Shared Ledger System

A monorepo-based **Shared Ledger System** designed to track user credits across multiple applications.  
This system ensures **type safety**, **code reuse**, and **extensibility** by allowing each application to add its own custom ledger operations on top of shared core operations.

New features include:  
- **Authentication & Authorization**  
- **Rate Limiting**  
- **Containerization with Docker and Docker Compose**  
- **Prometheus Monitoring**  
- **Grafana Dashboards**  
- **Advanced Logging**  
- **Redis Caching**

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
9. [Authentication Endpoints](#authentication-endpoints)  
10. [Rate Limiting](#rate-limiting)  
11. [Prometheus Monitoring](#prometheus-monitoring)  
12. [Grafana Dashboard](#grafana-dashboard)  
13. [Logging](#logging)  
14. [Redis Cache](#redis-cache)  
15. [Usage](#usage)  
16. [Redoc Documentation](#redoc-documentation)  
17. [Testing](#testing)  
18. [Migration Examples](#migration-examples)  
19. [Submission Guidelines](#submission-guidelines)  
20. [Recommendations](#recommendations)  
21. [Contributing](#contributing)  
22. [Acknowledgments](#acknowledgments)  
23. [AI Tools Used](#ai-tools-used)  
24. [License](#license)

---

## Project Purpose

- **Shared Ledger Logic**: Provide a single, core ledger implementation that all applications in the monorepo can leverage.
- **Type Safety**: Enforce a consistent, type-safe approach to shared ledger operations using Python Enums, Pydantic, and SQLAlchemy.
- **Extensibility**: Allow individual applications to define additional ledger operations without breaking shared functionality.
- **Database Integrity**: Ensure each transaction is tracked and stored with strict data integrity using Postgres and Alembic migrations.
- **Enhanced Security & Performance**: With integrated authentication, rate limiting, and Redis caching, the system is designed to be secure and performant.
- **Observability**: Utilize Prometheus for monitoring, Grafana for dashboards, and advanced logging for troubleshooting.

---

## Features

- ✅ **Type-safe ledger operations**  
- ✅ **Enforced shared operations**  
- ✅ **Authentication & Authorization**  
- ✅ **Rate Limiting for API endpoints**  
- ✅ **Containerized deployment using Docker and Docker Compose**  
- ✅ **Prometheus Monitoring for system metrics**  
- ✅ **Grafana Dashboards for visualization**  
- ✅ **Advanced logging mechanism**  
- ✅ **Redis Caching for improved performance**  
- ✅ **Async database operations with SQLAlchemy**  
- ✅ **Comprehensive test coverage**  
- ✅ **Alembic migrations**

---

## Technical Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy 2.0+**
- **Pydantic**
- **Alembic**
- **PostgreSQL**
- **Redis** (for caching)
- **Docker & Docker Compose**
- **Prometheus** (for monitoring)
- **Grafana** (for dashboards)
- **Python-Jose & Passlib** (for authentication)

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

```plaintext
shared-ledger-system/
         |    
         ├── README.md
         ├── pyproject.toml
         ├── requirements.txt
         ├── docker-compose.yml
         ├── entrypoint.sh
         ├── prometheus.yml
         ├── .gitignore
         ├── .env
         └── shared-ledger-system/
                     ├── apps/
                     │   ├── app1/
                     │   │   ├── src/
                     │   │   │   ├── __init__.py
                     │   │   │   ├──  config.py
                     │   │   │   ├──  Dockerfile
                     │   │   │   ├──  main.py
                     │   │   │   └──  api/
                     │   │   │         ├── __init__.py
                     │   │   │         └── core/
                     │   │   │               ├── __init__.py
                     │   │   │               └── ledgers/
                     │   │   │                       ├── __init__.py
                     │   │   │                       ├── dependencies.py
                     │   │   │                       ├── routes.py
                     │   │   │                       └── schemas.py
                     │   │   └── tests/
                     │   └── app2/
                     │       └── (similar structure)
                     ├── core/
                     │     ├── __init__.py
                     |     ├── config.py
                     │     ├── auth/
                     │     │     ├── __init__.py
                     │     │     ├── models.py
                     │     │     ├── routes.py                    
                     │     │     ├── schemas.py
                     │     │     └── service.py
                     │     ├── cache/
                     │     │     ├── __init__.py
                     │     │     └──  cache.py
                     │     ├── db/
                     │     │     ├── __init__.py
                     │     │     ├── base.py
                     │     │     └── migrations/
                     │     │             ├── __init__.py
                     │     │             ├── alembic_test.ini
                     │     │             ├── alembic.ini
                     │     │             ├── alembic/
                     │     │             │       ├── __init__.py
                     │     │             │       ├── env.py
                     │     │             │       └── versions/
                     │     │             │             ├── __init__.py
                     │     │             │             ├── 0001_initial.py
                     │     │             │             └── 0002_add_more_operations.py
                     │     │             └── alembic_test/
                     │     │                    ├── __init__.py
                     │     │                    └── env.py
                     │     │
                     │     ├── ledgers/
                     │     │       ├── __init__.py
                     │     │       ├── exceptions.py
                     │     │       ├── models.py
                     │     │       ├── operations.py
                     │     │       ├── schemas.py
                     │     │       └── service.py
                     │     ├── logging/
                     │     │     ├── __init__.py
                     │     │     └── logger.py
                     │     └── monitoring/
                     │              ├── __init__.py
                     │              └── prometheus.py
                     ├── tests/
                     │     ├── __init__.py
                     │     ├── conftest.py
                     │     ├── apps/
                     │     │     ├── app1/
                     │     │     │   ├── __init__.py
                     │     │     │   ├── test_api.py
                     │     │     │   ├── test_auth.py
                     │     │     │   ├── test_prometheus.py
                     │     │     │   └── test_rate_limit.py      
                     │     │     └── app2/
                     │     └── core/
                     │         ├── __init__.py
                     │         ├── auth/
                     │         │     └── test_auth_service.py
                     │         ├── cache/
                     │         │     └──  test_cache.py
                     │         ├── ledgers/
                     │         │     ├── test_operations.py
                     │         │     └── test_service.py
                     │         ├── logging/
                     │         │     └── test_logger.py
                     │         └── monitoring/
                     │             └── test_prometheus.py
                     └── pytest.ini
 ``` 

- **shared-ledger-system/**: The root directory.
  - **.env**: Environment variables for local development.
  - **.env.test**: Environment variables for testing.
  - **docker-compose.yml**: Docker Compose configuration including a test container that runs tests automatically.
- **core/**: Contains the core ledger functionality and new features.
- **apps/**: Contains multiple applications consuming the core ledger functionalities.
- **tests/**: Contains tests for core and application-specific features.

---

## Core Concepts

### Shared vs. Application-Specific Ledger Operations

- **Shared Operations**: `DAILY_REWARD`, `SIGNUP_CREDIT`, `CREDIT_SPEND`, `CREDIT_ADD`
- **App-Specific Operations**: For example, `CONTENT_CREATION`, `CONTENT_ACCESS`

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

---

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd shared-ledger-system 
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install necessary packages:**
   ```bash
   pip install fastapi[all] sqlalchemy[async] alembic pydantic python-jose[cryptography] passlib[bcrypt] pytest pytest-asyncio aioredis
   ```

4. **Generate requirements.txt:**
   ```bash
   pip freeze > requirements.txt
   ```

5. **Set up environment variables:**

   Create a `.env` file for local development and a `.env.test` file for testing.
   ```env
   # .env
   DATABASE_URL=postgresql+asyncpg://postgres:12345@localhost:5432/shared_ledger_system
   TEST_DATABASE_URL=postgresql+asyncpg://postgres:12345@localhost:5432/test_db
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=your_secret_key_here
   ```

6. **Run database migrations:**
   ```bash
   cd shared-ledger-system/core/db/migrations
   alembic upgrade head
   ```

7. **Docker Setup:**

   Run the entire system using Docker and Docker Compose:
   ```bash
   docker-compose up --build
   ```
   
   The `docker-compose.yml` starts containers for:
   - **app1**: The primary application.
   - **tests**: A dedicated test container that automatically runs tests.
   - **db**: PostgreSQL database.
   - **redis**: Redis caching.
   - **prometheus**: Monitoring with Prometheus.
   - **grafana**: Visualization and dashboarding with Grafana.

8. **Configure Application:**

   Adjust configuration files as needed.

---

## Running the Applications

1. **Start Required Services:**
   - Ensure Redis and PostgreSQL are running.
   - Prometheus and Grafana are started as part of the Docker Compose setup.
2. **Run the application:**
   ```bash
   cd shared-ledger-system
   uvicorn apps.app1.src.main:app --reload --host 0.0.0.0 --port 8000  
   ```
   
   The API is available at [http://localhost:8000](http://localhost:8000)  
   Swagger documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

### Ledger Endpoints

- **GET /ledger/{owner_id}**  
  Returns the current balance for the specified `owner_id`.

- **POST /ledger**  
  Creates a new ledger entry.  
  **Request Body (example):**
  ```json
  {
    "owner_id": "user123",
    "operation": "CREDIT_ADD",
    "amount": 10,
    "nonce": "unique-transaction-id"
  }
  ```
  **Behavior:**
  1. Checks for sufficient balance if the operation is negative.
  2. Prevents duplicate transactions using `nonce`.

---

## Authentication Endpoints

- **POST /auth/register**  
  Register a new user.  
  **Example Request:**
  ```bash
  curl -X POST http://localhost:8000/auth/register \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "Test@1234"}'
  ```

- **POST /auth/token**  
  Log in to retrieve an access token.  
  **Example Request:**
  ```bash
  curl -X POST http://localhost:8000/auth/token \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser&password=Test@1234"
  ```
  **Expected Response:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

- **GET /auth/me**  
  Retrieve details of the currently authenticated user.  
  **Example Request:**
  ```bash
  curl -X GET http://localhost:8000/auth/me \
    -H "Authorization: Bearer <your-access-token>"
  ```

---

## Rate Limiting

Rate limiting is implemented via middleware and decorators to protect API endpoints from abuse.  
Refer to `tests/apps/app1/test_rate_limit.py` for sample tests.

---

## Prometheus Monitoring

Prometheus monitors system metrics.  
- **Configuration:** `prometheus.yml`  
- **Integration:** `core/monitoring/prometheus.py`  
- **Usage:** Metrics are accessible at [http://localhost:8000/metrics](http://localhost:8000/metrics).

---

## Grafana Dashboard

Grafana provides visualizations for metrics collected by Prometheus.
- **Access:** [http://localhost:3000](http://localhost:3000)
- **Configuration:** Connect Grafana to the Prometheus data source (typically at `http://prometheus:9090` within the Docker network).

---

## Logging

Advanced logging facilitates troubleshooting.  
- **Location:** `core/logging/logger.py`  
- **Features:** Structured log output with configurable levels and formats.

---

## Redis Cache

Redis caching reduces database load and improves performance.  
- **Location:** `core/cache/cache.py`  
- **Setup:** Ensure `REDIS_URL` is correctly set in `.env`.

---

## Usage

### Register a New User

Send a POST request to `/auth/register`:

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "Test@1234"}'
```

### Log In to Retrieve an Access Token

Send a POST request to `/auth/token` with your credentials:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=Test@1234"
```

You will receive a JSON response with the access token:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Use the Ledger Endpoint to Add Credit

With the obtained access token, add credit by sending a POST request to `/ledger`:

```bash
curl -X POST http://localhost:8000/ledger/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-access-token>" \
  -d '{"owner_id": "testuser", "operation": "CREDIT_ADD", "amount": 10, "nonce": "unique-transaction-id"}'
```

On success, you will receive a confirmation message. Verify the updated balance:

```bash
curl -X GET http://localhost:8000/ledger/testuser \
  -H "Authorization: Bearer <your-access-token>"
```

---

## Redoc Documentation

FastAPI provides Redoc out of the box. Visit:  
```
http://localhost:8000/redoc
```

---

## Testing

1. **Run Tests:**
   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```
2. **Test Directories:**
   - **Core tests:** `tests/core/ledgers/`, `tests/core/auth/`, `tests/core/cache/`, etc.
   - **Application tests:** `apps/app1/tests/`, `apps/app2/tests/`

*Note:* The Docker Compose setup includes a dedicated test container that automatically runs tests when containers start.

---

## Migration Examples

1. **Create a New Migration:**
   ```bash
   cd core/db/migrations
   alembic revision -m "Add ledger table"
   ```
2. **Apply Migrations:**
   ```bash
   alembic upgrade head
   ```
3. **App-Specific:**  
   Each app can maintain separate migration scripts if needed.
4. **Real-World Example:**
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

   def downgrade() -> None:
       op.drop_index('idx_owner_id', table_name='ledger_entries')
       op.drop_index('idx_nonce', table_name='ledger_entries')
       op.drop_table('ledger_entries')
   ```

---

## Submission Guidelines

1. **Submit via GitHub repository.**
2. **Include:**
   - Implementation
   - Tests
   - Documentation
   - Migration examples
3. **Commit History:**  
   Demonstrate step-by-step development progress.

---

## Recommendations

- **Environment Management:** Use a virtual environment to isolate dependencies.
- **Dependency Management:** Employ a package manager (pip, poetry).
- **Code Formatting:** Use a formatter (e.g., Black) for consistent style.
- **Static Type Checking:** Use mypy or pyright to detect type errors.
- **Linting:** Use flake8 or pylint for code quality checks.

---

## Contributing

1. Fork the repository  
2. Create a new branch  
3. Commit your changes  
4. Push your changes  
5. Create a pull request

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Redis](https://redis.io/)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)

---

## AI Tools Used

This project leveraged several AI tools during development, documentation, and testing:

- **Windsurf**
- **Gemini**
- **ChatGPT** (by OpenAI)
- **Qwen**
- **DeepSeek**
- **Mistral**
- *(and other similar tools)*

---

## License

This project is provided under the [MIT License](LICENSE), unless stated otherwise in your repository.

---