import typer
from sqlalchemy.orm import Session

from facilibras.config.db import engine
from facilibras.controladores.autenticacao import hasher
from facilibras.dal import UsuarioDAO
from facilibras.modelos import Usuario


def criar_super_usuario():
    nome = typer.prompt("Nome")
    email = typer.prompt("Email")
    senha = typer.prompt(
        "Senha", hide_input=True, confirmation_prompt="Confirme sua senha"
    )

    with Session(engine) as session:
        usuario_dao = UsuarioDAO(session)
        usuario = Usuario(nome, email, hasher.hash(senha), True)
        usuario_dao.criar(usuario)
        typer.echo("Superusuário criado com sucesso!")


if __name__ == "__main__":
    criar_super_usuario()
