# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from app.adapters.driver.dependencies import get_db
from database import Base
from main import app


# --------------------------------------------------------------------------- #
# FIXTURES
# --------------------------------------------------------------------------- #


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def repo(db_session):
    from app.adapters.driven.repositories.payment import PaymentRepository

    return PaymentRepository(db_session)


@pytest.fixture
def client(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
