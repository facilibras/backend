from json import load
from string import ascii_uppercase

from alembic import command
from alembic.config import Config
from sqlalchemy.orm import Session

from facilibras.config.db import engine
from facilibras.modelos import (
    Exercicio,
    ExercicioStatus,
    ExercicioUsuario,
    Palavra,
    PalavraExercicio,
    Secao,
    Usuario,
)

if __name__ == "__main__":
    print("Aplicando as migrações do banco de dados")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    with open("links_drive.json", "r", encoding="utf-8") as f:
        links_drive = load(f)

    print("Populando o banco de dados")
    with Session(engine) as session:
        # Usuários e Seções
        usuario = Usuario("João", "joao@exemplo.com", "123")
        alfabeto = Secao("Alfabeto", "Aprenda e pratique as letras do alfabeto")
        numeros = Secao("Números", "Aprenda e pratique os números do 0 ao 9")

        alfabeto_dict = {
            f"letra_{letra}": Palavra(f"Letra{letra}", links_drive[letra])
            for letra in ascii_uppercase + "Ç"
        }
        numeros_dict = {
            f"numero_{numero}" : Palavra(str(numero), links_drive[str(numero)])
            for numero in range(10)
        }

        adicionar = [usuario, alfabeto, numeros]
        session.add_all(adicionar)
        session.commit()
        for obj in adicionar:
            session.refresh(obj)

        # Exercícios
        exercicios = []
        palavra_exercicios = []
        for sinal, palavra in (alfabeto_dict|numeros_dict).items():
            ex = Exercicio(
                alfabeto.id_secao,
                sinal.lower(),
                f"TODO: Instruções p/ {palavra.nome} em formato texto"
            )
            pe = PalavraExercicio(palavra=palavra, exercicio=ex)
            exercicios.append(ex)
            palavra_exercicios.append(pe)

        session.add_all(exercicios + palavra_exercicios)
        session.commit()

        # Progresso
        completos = [
            ExercicioUsuario(ExercicioStatus.COMPLETO, usuario, exercicios[i])
            for i in (2, 5, 8)
        ]
        abertos = [
            ExercicioUsuario(ExercicioStatus.ABERTO, usuario, exercicios[i])
            for i in (4, 10, 15)
        ]
        session.add_all(completos + abertos)
        session.commit()
    
    print("Migrações e inserção de dados iniciais aplicados com sucesso!")
