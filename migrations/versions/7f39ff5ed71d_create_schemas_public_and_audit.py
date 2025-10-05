"""create schemas public and audit

Revision ID: 7f39ff5ed71d
Revises: 
Create Date: 2025-10-04 21:31:07.679683

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '7f39ff5ed71d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS public;")
    op.execute("CREATE SCHEMA IF NOT EXISTS audit;")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS audit CASCADE;")
