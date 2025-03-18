import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from facilibras.main import app
from facilibras.modelos.usuario import registro_tabelas


@pytest.fixture
def cliente_http():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    registro_tabelas.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    registro_tabelas.metadata.drop_all(engine)
