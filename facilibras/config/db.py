from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from facilibras.config.env import get_variavel_ambiente

CAMINHO_DB = get_variavel_ambiente("CAMINHO_DB")

engine = create_engine(CAMINHO_DB)


def get_db_session():
    with Session(engine) as session:
        yield session
