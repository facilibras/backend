"""create sequences for tables

Revision ID: 310acab88caa
Revises: 7f39ff5ed71d
Create Date: 2025-10-04 21:35:47.330504

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '310acab88caa'
down_revision: Union[str, None] = '7f39ff5ed71d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("CREATE SEQUENCE IF NOT EXISTS public.sq_usuarios;")
    op.execute("CREATE SEQUENCE IF NOT EXISTS public.sq_perfis;")
    op.execute("CREATE SEQUENCE IF NOT EXISTS public.sq_palavras;")
    op.execute("CREATE SEQUENCE IF NOT EXISTS public.sq_secoes;")
    op.execute("CREATE SEQUENCE IF NOT EXISTS public.sq_exercicios;")


def downgrade() -> None:
    op.execute("DROP SEQUENCE IF EXISTS public.sq_exercicios;")
    op.execute("DROP SEQUENCE IF EXISTS public.sq_secoes;")
    op.execute("DROP SEQUENCE IF EXISTS public.sq_palavras;")
    op.execute("DROP SEQUENCE IF EXISTS public.sq_perfis;")
    op.execute("DROP SEQUENCE IF EXISTS public.sq_usuarios;")
