"""create audit trigger functions

Revision ID: 1206b2bbc648
Revises: e12388461c1e
Create Date: 2025-10-04 21:52:56.805901

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '1206b2bbc648'
down_revision: Union[str, None] = 'e12388461c1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Função de auditoria para tb_usuarios
    op.execute("""
    CREATE OR REPLACE FUNCTION public.fn_audit_tb_usuarios()
    RETURNS TRIGGER AS $$
    DECLARE
        v_id_usuario_acao INTEGER;
    BEGIN
        v_id_usuario_acao := 0; 

        IF (TG_OP = 'INSERT') THEN
            INSERT INTO audit.tb_usuarios (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, nome_usuario, email, criado_em, ultimo_login, ativo
            ) 
            VALUES (
                NOW(), v_id_usuario_acao, 'N', 'INSERT',
                NEW.id, NEW.nome_usuario, NEW.email,
                NEW.criado_em, NEW.ultimo_login, NEW.ativo
            );
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO audit.tb_usuarios (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, nome_usuario, email, criado_em, ultimo_login, ativo
            ) 
            VALUES (
                NOW(), v_id_usuario_acao, 'A', 'UPDATE',
                OLD.id, OLD.nome_usuario, OLD.email,
                OLD.criado_em, OLD.ultimo_login, OLD.ativo
            );
            INSERT INTO audit.tb_usuarios (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, nome_usuario, email, criado_em, ultimo_login, ativo
            ) 
            VALUES (
                NOW(), v_id_usuario_acao, 'N', 'UPDATE',
                NEW.id, NEW.nome_usuario, NEW.email,
                NEW.criado_em, NEW.ultimo_login, NEW.ativo
            );
            RETURN NEW;

        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO audit.tb_usuarios (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, nome_usuario, email, criado_em, ultimo_login, ativo
            ) VALUES (
                NOW(), v_id_usuario_acao, 'A', 'DELETE',
                OLD.id, OLD.nome_usuario, OLD.email,
                OLD.criado_em, OLD.ultimo_login, OLD.ativo
            );
            RETURN OLD;
        END IF;

        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Função de auditoria para tb_perfis
    op.execute("""
    CREATE OR REPLACE FUNCTION public.fn_audit_tb_perfis()
    RETURNS TRIGGER AS $$
    DECLARE
        v_id_usuario_acao INTEGER;
    BEGIN
        v_id_usuario_acao := 0;

        IF (TG_OP = 'INSERT') THEN
            INSERT INTO audit.tb_perfis (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, usuario_id, apelido, url_img_perfil, url_img_fundo, qtd_ex_completos, criado_em
            )
            VALUES (
                NOW(), v_id_usuario_acao, 'N', 'INSERT',
                NEW.id, NEW.usuario_id, NEW.apelido,
                NEW.url_img_perfil, NEW.url_img_fundo, 
                NEW.qtd_ex_completos, NEW.criado_em
            );
            RETURN NEW;

        ELSIF (TG_OP = 'UPDATE') THEN
            INSERT INTO audit.tb_perfis (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, usuario_id, apelido, url_img_perfil, url_img_fundo, qtd_ex_completos, criado_em
            )
            VALUES (
                NOW(), v_id_usuario_acao, 'N', 'UPDATE',
                NEW.id, NEW.usuario_id, NEW.apelido,
                NEW.url_img_perfil, NEW.url_img_fundo,
                NEW.qtd_ex_completos, NEW.criado_em
            );
            INSERT INTO audit.tb_perfis (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, usuario_id, apelido, url_img_perfil, url_img_fundo, qtd_ex_completos, criado_em
            )
            VALUES (
                NOW(), v_id_usuario_acao, 'A', 'UPDATE',
                OLD.id, OLD.usuario_id, OLD.apelido,
                OLD.url_img_perfil, OLD.url_img_fundo,
                OLD.qtd_ex_completos, OLD.criado_em
            );
            RETURN NEW;

        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO audit.tb_perfis (
                hr_alteracao, usuario_alteracao, tp_alteracao, acao,
                id, usuario_id, apelido, url_img_perfil, url_img_fundo, criado_em
            )
            VALUES (
                NOW(), v_id_usuario_acao, 'A', 'DELETE',
                OLD.id, OLD.usuario_id, OLD.apelido,
                OLD.url_img_perfil, OLD.url_img_fundo,
                OLD.qtd_ex_completos, OLD.criado_em
            );
            RETURN OLD;
        END IF;

        RETURN NULL;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Criar triggers para auditoria
    op.execute("""
    CREATE TRIGGER tr_audit_tb_usuarios
    AFTER INSERT OR UPDATE OR DELETE
    ON public.tb_usuarios
    FOR EACH ROW
    EXECUTE FUNCTION public.fn_audit_tb_usuarios();
    """)

    op.execute("""
    CREATE TRIGGER tr_audit_tb_perfis
    AFTER INSERT OR UPDATE OR DELETE
    ON public.tb_perfis
    FOR EACH ROW
    EXECUTE FUNCTION public.fn_audit_tb_perfis();
    """)


def downgrade():
    op.execute("DROP FUNCTION IF EXISTS public.fn_audit_tb_usuarios();")
    op.execute("DROP FUNCTION IF EXISTS public.fn_audit_tb_perfis();")
    op.execute("DROP TRIGGER IF EXISTS tr_audit_tb_usuarios ON public.tb_usuarios;")
    op.execute("DROP TRIGGER IF EXISTS tr_audit_tb_perfis ON public.tb_perfis;")
