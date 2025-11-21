from pathlib import Path
from string import ascii_lowercase

import typer

from facilibras.modelos.sinais import (
    SinalLibras,
    construir_sinal,
    get_sinal,
    listar_sinais,
    qtd_sinais,
)

app = typer.Typer(add_completion=False)


LETRAS = set(ascii_lowercase + "ç")
NUMEROS = {f"{i}" for i in range(10)} | {f"{i}_2" for i in range(1, 5)}
ALIMENTOS = {"água", "biscoito", "bolacha"}
SAUDACOES = {"tudo_bem", "oi", "tchau"}
VERBOS = {"aprender", "entender", "ouvir", "saber"}
FRASES = {"oi_tudo_bem"}
IDENTIDADES = {"você", "eu", "meu", "seu", "nome"}
OUTROS = {"muro", "porta"}


def validar_letra(letra: str):
    if letra.lower() not in LETRAS:
        exc = "A letra deve ser uma dos seguintes:" + " ".join(sorted(LETRAS))
        raise typer.BadParameter(exc)
    return letra


def validar_numero(numero: str):
    if numero not in NUMEROS:
        exc = "O número deve ser um dos seguintes:" + " ".join(sorted(NUMEROS))
        raise typer.BadParameter(exc)
    return numero


def validar_alimento(alimento: str):
    if alimento not in ALIMENTOS:
        exc = "O alimento deve ser um dos seguintes:" + " ".join(sorted(ALIMENTOS))
        raise typer.BadParameter(exc)
    return alimento


def validar_saudacao(saud: str):
    if saud not in SAUDACOES:
        exc = "A saudação deve ser uma das seguintes:" + " ".join(sorted(SAUDACOES))
        raise typer.BadParameter(exc)
    return saud


def validar_verbo(verbo: str):
    if verbo not in VERBOS:
        exc = "O verbo deve ser um dos seguintes:" + " ".join(sorted(VERBOS))
        raise typer.BadParameter(exc)
    return verbo


def validar_frase(frase: str):
    if frase not in FRASES:
        exc = "A frase deve ser uma das seguintes:" + " ".join(sorted(FRASES))
        raise typer.BadParameter(exc)
    return frase


def validar_identidade(identidade: str):
    if identidade not in IDENTIDADES:
        exc = "A identidade deve ser uma das seguintes:" + " ".join(sorted(IDENTIDADES))
        raise typer.BadParameter(exc)
    return identidade


def validar_outros(outro: str):
    if outro not in OUTROS:
        exc = "O sinal deve ser um dos seguintes:" + " ".join(sorted(OUTROS))
        raise typer.BadParameter(exc)
    return outro


def reconhecer(sinal: SinalLibras, video: str | None):
    from facilibras.controladores.reconhecimento import (
        reconhecer_video,
        reconhecer_webcam,
    )

    if video:
        if not Path(video).exists():
            typer.secho("Caminho do vídeo não encontrado!", fg=typer.colors.BRIGHT_RED)
            exit(1)

        typer.echo(f"Vídeo: {video}")
        feedback = reconhecer_video(sinal, video)
    else:
        feedback = reconhecer_webcam(sinal)

    if feedback.sucesso:
        typer.secho("Sucesso!", fg=typer.colors.BRIGHT_GREEN)
        for f in feedback.feedback:
            typer.secho(f.mensagem, fg=typer.colors.BRIGHT_GREEN)
    else:
        typer.secho("Falhou!", fg=typer.colors.BRIGHT_RED)
        for f in feedback.feedback:
            cor = typer.colors.BRIGHT_GREEN if f.correto else typer.colors.BRIGHT_RED
            typer.secho(f.mensagem, fg=cor)

    return feedback.sucesso


@app.command()
def letra(
    letra: str = typer.Argument(..., callback=validar_letra),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo a letra: {letra.upper()}")
    sinal = get_sinal(f"letra_{letra.lower()}")
    return reconhecer(sinal, video)


@app.command()
def numero(
    numero: str = typer.Argument(..., callback=validar_numero),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo o número: {numero.upper()}")
    sinal = get_sinal(f"número_{numero.lower()}")
    return reconhecer(sinal, video)


@app.command()
def alimento(
    alimento: str = typer.Argument(..., callback=validar_alimento),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo o alimento: {alimento.upper()}")
    sinal = get_sinal(alimento.lower())
    return reconhecer(sinal, video)


@app.command()
def saudacao(
    saudacao: str = typer.Argument(..., callback=validar_saudacao),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo a saudação: {saudacao.upper()}")
    sinal = get_sinal(saudacao.lower())
    return reconhecer(sinal, video)


@app.command()
def frase(
    frase: str = typer.Argument(..., callback=validar_frase),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo a frase: {frase.upper()}")
    sinal = get_sinal(frase.lower())
    return reconhecer(sinal, video)


@app.command()
def identidade(
    identidade: str = typer.Argument(..., callback=validar_identidade),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo a identidade: {identidade.upper()}")
    sinal = get_sinal(identidade.lower())
    return reconhecer(sinal, video)


@app.command()
def outros(
    outros: str = typer.Argument(..., callback=validar_outros),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo o sinal: {outros.upper()}")
    sinal = get_sinal(outros.lower())
    return reconhecer(sinal, video)


@app.command()
def verbo(
    verbo: str = typer.Argument(..., callback=validar_verbo),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado ao sinal"
    ),
) -> bool:
    typer.echo(f"Reconhecendo o sinal: {verbo.upper()}")
    sinal = get_sinal(verbo.lower())
    return reconhecer(sinal, video)


@app.command()
def sinais():
    typer.echo(f"Listando todos os {qtd_sinais()} sinais")
    typer.echo(listar_sinais())


@app.command()
def interativo(
    o: str = typer.Option(
        "FRENTE", "-o", "--orientacao", help="Orientação da palma da mão"
    ),
    i: str = typer.Option(
        "RETA", "-i", "--inclinacao", help="Inclinação da palma da mão"
    ),
    d: list[str] | None = typer.Option(
        [], "-d", "--dedo", help="Lista de posições dos dedos"
    ),
    p: list[str] | None = typer.Option(
        [], "-p", "--posicao", help="Posição da mão e ponto de referência"
    ),
    e: str = typer.Option("QUALQUER", "-e", "--expressao", help="Expressão facial"),
):
    if not d and not o:
        typer.secho("Dedo ou orientação necessários", fg=typer.colors.BRIGHT_RED)
        exit(1)

    if p:
        pos = p[0]
        if len(p) == 2:
            pf = int(p[1])
        elif len(p) == 1:
            pf = 0
        else:
            typer.secho(
                "Informe posição e ponto de referência", fg=typer.colors.BRIGHT_RED
            )
            exit(1)
    else:
        pos = "QUALQUER"
        pf = 0

    from facilibras.controladores.reconhecimento import reconhecer_interativamente

    d = [dedo.upper() for dedo in d] if d else []

    sinal = construir_sinal(d, i.upper(), o.upper(), pos.upper(), e.upper(), pf)
    typer.secho("Reconhecendo o sinal:", fg=typer.colors.BRIGHT_GREEN)
    typer.echo(sinal)
    reconhecer_interativamente(sinal)
