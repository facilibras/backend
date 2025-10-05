from collections import defaultdict
from json import load

from alembic import command
from alembic.config import Config
from pwdlib import PasswordHash
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from facilibras.config.db import engine
from facilibras.modelos import (
    Exercicio,
    ExercicioStatus,
    Palavra,
    ProgressoUsuario,
    Secao,
    Usuario,
)
from facilibras.modelos.perfil import Perfil

if __name__ == "__main__":
    print("Aplicando as migrações do banco de dados")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    hasher = PasswordHash.recommended()

    with open("data/sinais.json", "r", encoding="utf-8") as f:
        dados = load(f)

    with Session(engine) as session:
        usuarios = []
        perfils = []
        # Usuarios
        nomes = ["Ana", "Beto", "Carlos", "Duda", "Eduardo"]
        for nome in nomes:
            perfil = Perfil(
                apelido=nome,
                url_img_perfil=f"https://placehold.co/50x50?text={nome[0]}",
            )
            usuario = Usuario(
                nome_usuario=nome.lower(),
                email=f"{nome.lower()}@exemplo.com",
                senha=hasher.hash("123"),
                perfil=perfil,
            )
            perfils.append(perfil)
            usuarios.append(usuario)

        session.add_all(perfils + usuarios)
        session.commit()

        # Secoes
        alfabeto = Secao("Alfabeto", "Aprenda e pratique as letras do alfabeto")
        numeros = Secao("Números", "Aprenda e pratique os números do 0 ao 9")
        comidas = Secao("Alimentos", "Aprenda e pratique sinais referentes a alimentos")
        verbos = Secao("Verbos", "Aprenda e pratique sinais referentes a verbos")
        saudacoes = Secao(
            "Saudações", "Aprenda e pratique sinais referentes a saudações"
        )
        identidade = Secao(
            "Identidade", "Aprenda e pratique sinais referentes a identidade"
        )
        outros = Secao("Outros", "Aprenda e pratique diversos sinais")

        # Salva secoes e usuarios
        adicionar = [
            alfabeto,
            numeros,
            comidas,
            verbos,
            saudacoes,
            identidade,
            outros,
            *perfils,
            *usuarios,
        ]
        session.add_all(adicionar)
        session.commit()
        for obj in adicionar:
            session.refresh(obj)

        # Palavras e exercicios
        sec_url = {
            "Alfabeto": "letra_",
            "Números": "numero_",
            "Alimentos": "alimento_",
            "Verbos": "verbo_",
            "Saudações": "saud_",
            "Identidade": "id_",
            "Outros": "",
        }
        sec_obj = {
            "Alfabeto": alfabeto,
            "Números": numeros,
            "Alimentos": comidas,
            "Verbos": verbos,
            "Saudações": saudacoes,
            "Identidade": identidade,
            "Outros": outros,
        }

        palavras: dict[int, list[Palavra]] = defaultdict(list)
        for chave in dados:
            sec_str = dados[chave]["categoria"]
            sec_url_str = sec_url[sec_str]
            sec_obj_str = sec_obj[sec_str]  # instância de Secao
            sec_id = sec_obj_str.id  # usa o id como chave

            var_1 = dados[chave]["1"]
            instrucoes_str = "\n".join(var_1["instrucoes"])
            palavras[sec_id].append(
                Palavra(f"{sec_url_str}{chave.lower()}", instrucoes_str, var_1["video"])
            )

            var_2 = dados[chave].get("2")
            if var_2:
                instrucoes_str = "\n".join(var_2["instrucoes"])
                palavras[sec_id].append(
                    Palavra(
                        f"{sec_url_str}{chave.lower()}_2",
                        instrucoes_str,
                        var_2["video"],
                    )
                )

        # Exercícios
        exercicios = []
        for sec_id, sinais in palavras.items():
            secao = session.get(Secao, sec_id)
            for sinal in sinais:
                ex = Exercicio(
                    titulo=sinal.nome, descricao=sinal.instrucoes, secao=secao or outros
                )
                ex.palavras.append(sinal)
                exercicios.append(ex)

        session.add_all(exercicios)
        session.commit()

        # Prox. Exercicios
        exercicios_alfabeto = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == alfabeto.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_alfabeto:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_numero = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == numeros.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_numero:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_comidas = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == comidas.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_comidas:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_verbos = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == verbos.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_verbos:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_saudacoes = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == saudacoes.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_saudacoes:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_identidade = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == identidade.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_identidade:
            ex.prox_exercicio = anterior
            anterior = ex

        exercicios_outros = session.scalars(
            select(Exercicio)
            .where(Exercicio.secao_id == outros.id)
            .order_by(desc(Exercicio.id))
        ).all()

        anterior = None
        for ex in exercicios_outros:
            ex.prox_exercicio = anterior
            anterior = ex

        session.commit()

        # Ranking
        completos = []
        rank = [[1, 2, 3], [1, 2, 3, 4], [1, 2], [1, 2, 3, 4, 5, 6], [1, 2]]
        for u, exs in enumerate(rank):
            for e in exs:
                completos.append(  # noqa: PERF401
                    ProgressoUsuario(
                        status=ExercicioStatus.COMPLETO,
                        usuario=usuarios[u],
                        exercicio=exercicios[e],
                    )
                )

        session.add_all(completos)
        session.commit()

    print("Migrações e inserção de dados iniciais aplicados com sucesso!")
