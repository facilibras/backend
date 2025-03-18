from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from facilibras.config.env import get_variavel_ambiente

URL_DB = get_variavel_ambiente("URL_DB")

registro_tabelas = registry()

engine = create_engine(URL_DB)


def get_db_session():
    with Session(engine) as session:
        yield session
