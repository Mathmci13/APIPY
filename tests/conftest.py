import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import Product

# Configuração do banco de dados para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Banco de dados local para testes
# Alternativa: SQLite em memória (não persiste entre os testes)
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture para o banco de dados
@pytest.fixture(scope="function")
def test_db_session():
    """
    Configura uma sessão de banco de dados para os testes.
    Cria as tabelas antes e remove após o teste.
    """
    Base.metadata.create_all(bind=engine)  # Cria as tabelas
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Remove as tabelas após os testes


# Substitui a dependência do banco de dados no FastAPI
@pytest.fixture(scope="function")
def override_get_db(test_db_session):
    """
    Substitui a dependência de banco de dados do FastAPI para usar o banco de testes.
    """
    def _get_db():
        try:
            yield test_db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _get_db


# Cliente de teste do FastAPI
@pytest.fixture(scope="function")
def test_client(override_get_db):
    """
    Retorna um cliente de teste configurado para o FastAPI.
    """
    with TestClient(app) as client:
        yield client


# Fixture para criar produtos de exemplo
@pytest.fixture(scope="function")
def add_sample_products(test_db_session):
    """
    Adiciona produtos de exemplo ao banco de dados para os testes.
    """
    def _add():
        products = [
            Product(name="Produto 1", description="Descrição 1", price=10.0, quantity=5),
            Product(name="Produto 2", description="Descrição 2", price=20.0, quantity=3),
        ]
        test_db_session.add_all(products)
        test_db_session.commit()
    return _add
