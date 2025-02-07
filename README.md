# Shared Ledger System

A shared ledger system that tracks user credits with type-safe operations and enforced shared operations across the system.

## Features

- ✅ Type-safe ledger operations
- ✅ Enforced shared operations
- ✅ Redis caching for performance optimization
- ✅ Rate limiting for API endpoints
- ✅ Prometheus metrics for monitoring
- ✅ Detailed JSON logging
- ✅ Async database operations with SQLAlchemy
- ✅ Comprehensive test coverage
- ✅ Alembic migrations

## Technical Stack

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0+
- Pydantic
- Alembic
- PostgreSQL
- Redis
- Prometheus

## Project Structure
shared-ledger/ 
├── core/ # Core business logic │ 
├── ledgers/ # Ledger related modules │ 
├── monitoring/ # Prometheus metrics │ 
├── logging/ # Logging configuration │ 
└── db/ # Database configuration 
├── src/ # API application 
├── alembic/ # Database migrations 
└── tests/ # Test suite


## Installation

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
6. Run the application:
```
uvicorn src.main:app --reload
```

## Usage    

1. Create a new ledger entry:
```     
curl -X POST http://localhost:8000/ledger/ -H "Content-Type: application/json" -d '{"operation": "CREDIT_ADD", "amount": 10, "owner_id": "test_user", "nonce": "123e4567-e89b-12d3-a456-426655440000"}'
```

2. Get the current balance of a user:
```
curl -X GET http://localhost:8000/ledger/test_user
```             

## Contributing

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push your changes
5. Create a pull request    
6. Request a pull requirements    

## License

This project is licensed under the [MIT License](LICENSE).  

## Acknowledgments  

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Redis](https://redis.io/)
- [Prometheus](https://prometheus.io/)  

