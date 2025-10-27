from collections import defaultdict
from json import load
from sys import argv

from alembic import command
from alembic.config import Config
from pwdlib import PasswordHash
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from facilibras.config.db import engine
from facilibras.modelos import (
    Conquista,
    Exercicio,
    ExercicioStatus,
    NomeConquista,
    Palavra,
    ProgressoUsuario,
    Secao,
    Usuario,
)
from facilibras.modelos.palavra_exercicio import PalavraExercicio
from facilibras.modelos.perfil import Perfil

if __name__ == "__main__":
    print("Aplicando as migrações do banco de dados")

    somente_tabelas = False
    if len(argv) > 1 and argv[1] in ("--sem_usuarios", "-su"):
        print("Iniciando somente tabelas")
        somente_tabelas = True

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    hasher = PasswordHash.recommended()

    with open("data/sinais.json", "r", encoding="utf-8") as f:
        dados = load(f)

    with Session(engine) as session:
        adicionar = []
        usuarios = []
        perfils = []
        conquistas = []
        if not somente_tabelas:
            # Usuarios
            nomes = ["Ana", "Beto", "Carlos", "Duda", "Eduardo"]
            rank = [
                [1, 55, 3],
                [1, 55, 3, 4],
                [55, 2],
                [1, 2, 3, 4, 5, 6],
                list(range(2, 28)),
            ]
            for idx, nome in enumerate(nomes):
                qtd = len(rank[idx])
                pontos_total = qtd * 100
                if nome == "Eduardo":
                    nivel = 5
                    sobrando = 100
                else:
                    nivel = 3
                    sobrando = pontos_total - 500
                    if pontos_total <= 100:
                        nivel = 1
                        sobrando = pontos_total
                    elif pontos_total <= 500:
                        nivel = 2
                        sobrando = pontos_total - 100

                perfil = Perfil(
                    apelido=nome,
                    url_img_perfil=f"https://placehold.co/50x50?text={nome[0]}",
                    qtd_ex_completos=qtd,
                    pontos_total=pontos_total,
                    pontos_nivel=sobrando,
                    nivel=nivel,
                )
                usuario = Usuario(
                    nome_usuario=nome.lower(),
                    email=f"{nome[0].lower()}@facilibras.com",
                    senha=hasher.hash("123"),
                    perfil=perfil,
                )

                # Conquistas
                conq_nomes = [NomeConquista.PRIMEIRO_SINAL, NomeConquista.ALIMENTOS]

                if nome in ("Ana", "Beto", "Carlos"):
                    c1 = Conquista(
                        nome=conq_nomes[0], descricao="Realizou seu primeiro sinal!"
                    )
                    c2 = Conquista(
                        nome=conq_nomes[1],
                        descricao="Completou todos os sinais da categoria Alimentos!",
                    )
                    perfil.conquistas = [c1, c2]
                    conquistas.extend([c1, c2])
                else:
                    c1 = Conquista(
                        nome=conq_nomes[0], descricao="Realizou seu primeiro sinal!"
                    )
                    perfil.conquistas = [c1]
                    conquistas.append(c1)

                perfils.append(perfil)
                usuarios.append(usuario)

            session.add_all(perfils + usuarios + conquistas)
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
        frases = Secao("Frases", "Aprenda e pratique múltiplos sinais de uma única vez")

        # Salva secoes e usuarios
        adicionar = [
            alfabeto,
            numeros,
            comidas,
            verbos,
            saudacoes,
            identidade,
            outros,
            frases,
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
            "Números": "número_",
            "Alimentos": "alimento_",
            "Verbos": "verbo_",
            "Saudações": "saud_",
            "Identidade": "id_",
            "Outros": "",
            "Frases": "",
        }
        sec_obj = {
            "Alfabeto": alfabeto,
            "Números": numeros,
            "Alimentos": comidas,
            "Verbos": verbos,
            "Saudações": saudacoes,
            "Identidade": identidade,
            "Outros": outros,
            "Frases": frases,
        }

        palavras: dict[int, list[Palavra]] = defaultdict(list)
        map_var = {}
        for chave in dados:
            sec_str = dados[chave]["categoria"]
            sec_url_str = sec_url[sec_str]
            sec_obj_str = sec_obj[sec_str]
            sec_id = sec_obj_str.id

            var_1 = dados[chave]["1"]
            if sec_str not in ("Números", "Alfabeto"):
                sec_url_str = ""
            titulo_str = chave.lower().replace(" ", "_")
            instrucoes_str = "\n".join(var_1["instrucoes"])
            palavras[sec_id].append(
                Palavra(f"{sec_url_str}{titulo_str}", instrucoes_str, var_1["video"])
            )

            var_2 = dados[chave].get("2")
            if var_2:
                titulo_str2 = sec_url_str + titulo_str + "_2"
                map_var[sec_url_str + titulo_str] = titulo_str2
                instrucoes_str = "\n".join(var_2["instrucoes"])
                palavras[sec_id].append(
                    Palavra(
                        titulo_str2,
                        instrucoes_str,
                        var_2["video"],
                    )
                )

        # Exercícios
        exercicios = []
        palavra_exercicios = []
        for sec_id, sinais in palavras.items():
            secao = session.get(Secao, sec_id)
            for sinal in sinais:
                ex = Exercicio(
                    titulo=sinal.nome,
                    descricao=sinal.instrucoes,
                    secao=secao or outros,
                    nome_variacao=map_var.get(sinal.nome, ""),
                    eh_variacao=sinal.nome in map_var.values(),
                )
                pe = PalavraExercicio(palavra=sinal, exercicio=ex)
                exercicios.append(ex)
                palavra_exercicios.append(ex)

        session.add_all(exercicios + palavra_exercicios)
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
        if not somente_tabelas:
            completos = []
            for u, exs in enumerate(rank):
                for e in exs:
                    completos.append(  # noqa: PERF401
                        ProgressoUsuario(
                            status=ExercicioStatus.COMPLETO,
                            usuario=usuarios[u],
                            exercicio=exercicios[e - 1],
                        )
                    )

            session.add_all(completos)
            session.commit()

    print("Migrações e inserção de dados iniciais aplicados com sucesso!")
