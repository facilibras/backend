"""create main and audit tables

Revision ID: e12388461c1e
Revises: 310acab88caa
Create Date: 2025-10-04 21:38:59.591192

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e12388461c1e'
down_revision: Union[str, None] = '310acab88caa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ----- Tabelas principais -----
    op.execute("""
    CREATE TABLE public.tb_usuarios (
        id INTEGER NOT NULL DEFAULT NEXTVAL('public.sq_usuarios'),
        nome_usuario VARCHAR(30) NOT NULL,
        email VARCHAR(100) NOT NULL,
        senha TEXT NOT NULL,
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        ultimo_login TIMESTAMP,
        ativo BOOLEAN NOT NULL DEFAULT TRUE,
        CONSTRAINT pk_id_usuario PRIMARY KEY (id),
        CONSTRAINT uk_nome_usuario UNIQUE (nome_usuario)
    );
    """)

    op.execute("""
    CREATE TABLE public.tb_perfis (
        id INTEGER NOT NULL DEFAULT NEXTVAL('public.sq_perfis'),
        usuario_id INTEGER NOT NULL,
        apelido VARCHAR(100) NOT NULL,
        url_img_perfil VARCHAR(200),
        url_img_fundo VARCHAR(200),
        qtd_ex_completos INTEGER NOT NULL DEFAULT 0,
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT pk_id_perfil PRIMARY KEY (id),
        CONSTRAINT fk_pefil_usuario FOREIGN KEY (usuario_id) REFERENCES tb_usuarios (id)
    );
    """)

    op.execute("""
    CREATE TABLE public.tb_palavras (
        id INTEGER NOT NULL DEFAULT NEXTVAL('public.sq_palavras'),
        nome VARCHAR(50) NOT NULL,
        url_video VARCHAR(200),
        CONSTRAINT pk_id_palavra PRIMARY KEY (id)
    );
    """)

    op.execute("""
    CREATE TABLE public.tb_secoes (
        id INTEGER NOT NULL DEFAULT NEXTVAL('public.sq_secoes'),
        nome VARCHAR(50) NOT NULL,
        descricao TEXT,
        CONSTRAINT pk_id_secao PRIMARY KEY (id)
    );
    """)

    op.execute("""
    CREATE TABLE public.tb_exercicios (
        id INTEGER NOT NULL DEFAULT NEXTVAL('public.sq_exercicios'),
        secao_id INTEGER NOT NULL,
        titulo VARCHAR(50) NOT NULL,
        descricao TEXT,
        prox_exercicio INTEGER,
        CONSTRAINT pk_id_exercicio PRIMARY KEY (id),
        CONSTRAINT fk_exercicio_secao FOREIGN KEY (secao_id) REFERENCES tb_secoes (id)
    );
    """)

    op.execute("""
    ALTER TABLE public.tb_exercicios
    ADD CONSTRAINT fk_prox_exercicio 
    FOREIGN KEY (prox_exercicio) 
    REFERENCES tb_exercicios (id);
    """)

    op.execute("""
    CREATE TABLE public.tb_progresso_usuarios (
        usuario_id INTEGER NOT NULL,
        exercicio_id INTEGER NOT NULL,
        status VARCHAR(1) NOT NULL DEFAULT 'I',
        criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        alterado_em TIMESTAMP,
        CONSTRAINT fk_progresso_id_usu FOREIGN KEY (usuario_id) REFERENCES tb_usuarios (id),
        CONSTRAINT fk_progresso_id_exe FOREIGN KEY (exercicio_id) REFERENCES tb_exercicios (id),
        CONSTRAINT pk_progresso_usuarios PRIMARY KEY (usuario_id, exercicio_id),
        CONSTRAINT ck_progresso_status CHECK (status IN ('I', 'C'))
    );
    """)

    op.execute("""
    COMMENT ON COLUMN public.tb_progresso_usuarios.status IS 'I - Incompleto; C - Completo';
    """)

    # ----- Tabelas de auditoria -----
    op.execute("""
    CREATE TABLE audit.tb_base (
        audit_id SERIAL PRIMARY KEY,
        hr_alteracao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        usuario_alteracao INTEGER,
        tp_alteracao VARCHAR(1) NOT NULL CHECK (tp_alteracao IN ('A', 'N')),
        acao VARCHAR(25) NOT NULL
    );
    """)

    op.execute("""
    COMMENT ON COLUMN audit.tb_base.tp_alteracao IS 'A - Antigo; N - Novo';
    COMMENT ON COLUMN audit.tb_base.acao IS 'Ação realizada na tabela. Exemplos: INSERT, UPDATE ou DELETE.';
    """)

    op.execute("""
    CREATE TABLE audit.tb_usuarios (
        LIKE audit.tb_base INCLUDING DEFAULTS,
        id INTEGER,
        nome_usuario VARCHAR(30),
        email VARCHAR(100),
        senha TEXT,
        criado_em TIMESTAMP,
        ultimo_login TIMESTAMP,
        ativo BOOLEAN
    );
    """)

    op.execute("""
    CREATE TABLE audit.tb_perfis (
        LIKE audit.tb_base INCLUDING DEFAULTS,
        id INTEGER,
        usuario_id INTEGER,
        apelido VARCHAR(100),
        url_img_perfil VARCHAR(200),
        url_img_fundo VARCHAR(200),
        qtd_ex_completos INTEGER,
        criado_em TIMESTAMP,
        atualizado_em TIMESTAMP
    );
    """)


def downgrade():
    # Tabelas audit 
    op.execute("DROP TABLE IF EXISTS audit.tb_perfis;")
    op.execute("DROP TABLE IF EXISTS audit.tb_usuarios;")
    op.execute("DROP TABLE IF EXISTS audit.tb_base;")

    # Tabelas principais
    op.execute("ALTER TABLE public.tb_exercicios DROP CONSTRAINT IF EXISTS fk_prox_exercicio;")
    op.execute("DROP TABLE IF EXISTS public.tb_progresso_usuarios;")
    op.execute("DROP TABLE IF EXISTS public.tb_exercicios;")
    op.execute("DROP TABLE IF EXISTS public.tb_secoes;")
    op.execute("DROP TABLE IF EXISTS public.tb_palavras;")
    op.execute("DROP TABLE IF EXISTS public.tb_perfis;")
    op.execute("DROP TABLE IF EXISTS public.tb_usuarios;")
