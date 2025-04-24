from string import ascii_lowercase

import typer

from facilibras.modelos.sinais import Categoria, get_sinal, listar_sinais

app = typer.Typer()


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
        typer.echo(f"Vídeo: {video}")
        res = reconhecer_video(sinal, video)
    else:
        res = reconhecer_webcam(sinal)

    if res:
        typer.secho("Reconhecido com sucesso!", fg=typer.colors.BRIGHT_GREEN)
    else:
        typer.secho("Não reconheceu o sinal!", fg=typer.colors.BRIGHT_RED)


@app.command()
def sinais(categoria: Categoria | None = typer.Option(None)):
    if categoria:
        typer.echo(f"Listando sinais da categoria: {categoria}")
        typer.echo(listar_sinais())
    else:
        typer.echo("Listando todos os sinais")
        typer.echo(listar_sinais())
