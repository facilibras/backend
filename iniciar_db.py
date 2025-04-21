from json import load
from string import ascii_uppercase

from alembic import command
from alembic.config import Config
from sqlalchemy import desc, select
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

    with Session(engine) as session:
        # Usuários e Seções
        usuario = Usuario("João", "joao@exemplo.com", "123")
        alfabeto = Secao("Alfabeto", "Aprenda e pratique as letras do alfabeto")
        numeros = Secao("Números", "Aprenda e pratique os números do 0 ao 9")

        alfabeto_dict = {
            f"letra_{letra.lower()}": Palavra(f"Letra{letra}", links_drive[letra])
            for letra in ascii_uppercase + "Ç"
        }
        numeros_dict = {
            f"numero_{numero}": Palavra(str(numero), links_drive[str(numero)])
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
        for sinal, palavra in alfabeto_dict.items():
            ex = Exercicio(
                titulo=sinal,
                descricao=f"TODO: Instruções p/ {palavra.nome} em formato texto",
                secao=alfabeto,
            )

            pe = PalavraExercicio(palavra=palavra, exercicio=ex)
            exercicios.append(ex)
            palavra_exercicios.append(pe)

        for sinal, palavra in numeros_dict.items():
            ex = Exercicio(
                titulo=sinal,
                descricao=f"TODO: Instruções p/ {palavra.nome} em formato texto",
                secao=numeros,
            )
            pe = PalavraExercicio(palavra=palavra, exercicio=ex)
            exercicios.append(ex)
            palavra_exercicios.append(pe)

        session.add_all(exercicios + palavra_exercicios)
        session.commit()

        # Prox. Exercicios
        exercicios_alfabeto = session.scalars(
            select(Exercicio)
            .where(Exercicio.id_secao == alfabeto.id_secao)
            .order_by(desc(Exercicio.id_exercicio))
        ).all()

        anterior = None
        for ex in exercicios_alfabeto:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_numero = session.scalars(
            select(Exercicio)
            .where(Exercicio.id_secao == numeros.id_secao)
            .order_by(desc(Exercicio.id_exercicio))
        ).all()

        anterior = None
        for ex in exercicios_numero:
            ex.prox_exercicio = anterior
            anterior = ex

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
