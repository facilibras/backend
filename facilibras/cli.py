from pathlib import Path
from string import ascii_lowercase

import typer

from facilibras.modelos.sinais import (
    Categoria,
    construir_sinal,
    get_sinal,
    listar_sinais,
)

app = typer.Typer(add_completion=False)


LETRAS_VALIDAS = set(ascii_lowercase + "ç")


def validar_letra(letra: str):
    if letra.lower() not in LETRAS_VALIDAS:
        exc = "A letra deve ser uma das seguintes:" + "".join(sorted(LETRAS_VALIDAS))
        raise typer.BadParameter(exc)
    return letra


@app.command()
def letra(
    letra: str = typer.Argument(..., callback=validar_letra),
    video: str | None = typer.Option(
        None, "--video", "-v", help="URL do vídeo associado à letra"
    ),
):
    from facilibras.controladores.reconhecimento import (
        reconhecer_video,
        reconhecer_webcam,
    )

    typer.echo(f"Reconhecendo a letra: {letra.upper()}")
    sinal = get_sinal(f"letra_{letra.lower()}")
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


@app.command()
def sinais(categoria: Categoria | None = typer.Option(None)):
    if categoria:
        typer.echo(f"Listando sinais da categoria: {categoria}")
        typer.echo(listar_sinais())
    else:
        typer.echo("Listando todos os sinais")
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
