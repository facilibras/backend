from sqlalchemy import select

from facilibras.modelos import Usuario


def test_criar_usuario(session):
    usuario = Usuario(nome="lucas", senha="123")
    session.add(usuario)
    session.commit()

    usuario = session.scalar(select(Usuario).where(Usuario.nome == "lucas"))
    assert usuario.nome == "lucas"
