"""create roles and permissions

Revision ID: 404de5d71f4f
Revises: 1206b2bbc648
Create Date: 2025-10-04 22:04:40.329163

"""
from typing import Sequence, Union
import os

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '404de5d71f4f'
down_revision: Union[str, None] = '1206b2bbc648'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    senha_dba = os.getenv("DBA_SENHA", "senha_dba")
    senha_app = os.getenv("APP_SENHA", "senha_app")

    # Criar roles se não existirem
    op.execute(f"""
    DO
    $do$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'dba_facilibras') THEN
            CREATE ROLE dba_facilibras WITH LOGIN PASSWORD '{senha_dba}';
        END IF;

        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app_facilibras') THEN
            CREATE ROLE app_facilibras WITH LOGIN PASSWORD '{senha_app}';
        END IF;
    END
    $do$;
    """)

    # Permissões
    op.execute("""
    -- Permissões de sequências
    GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO dba_facilibras;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO dba_facilibras;

    GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO app_facilibras;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO app_facilibras;

    -- Permissões de tabelas
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO dba_facilibras;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dba_facilibras;

    GRANT SELECT ON ALL TABLES IN SCHEMA public TO PUBLIC;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO PUBLIC;

    GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO app_facilibras;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO app_facilibras;

    GRANT SELECT ON ALL TABLES IN SCHEMA "audit" TO PUBLIC;
    ALTER DEFAULT PRIVILEGES IN SCHEMA "audit" GRANT SELECT ON TABLES TO PUBLIC;
    """)


def downgrade():
    op.execute("DROP ROLE IF EXISTS dba_facilibras;")
    op.execute("DROP ROLE IF EXISTS app_facilibras;")

