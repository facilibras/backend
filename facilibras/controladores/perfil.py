import uuid
from http import HTTPStatus
from pathlib import Path

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse, RedirectResponse

from facilibras.controladores.pontuacao import calcular_porcentagem, pontos_para_subir
from facilibras.dependencias.dal import T_ExercicioDAO, T_UsuarioDAO
from facilibras.modelos import Perfil
from facilibras.schemas.generico import MensagemSchema
from facilibras.schemas.perfil import (
    AtividadeSchema,
    AtualizarPerfilSchema,
    ConquistaSchema,
    PerfilSchema,
    ProgressoSchema,
)

PASTA_IMAGENS = Path("imagens")
PASTA_IMAGENS.mkdir(exist_ok=True)


class PerfilControle:
    """Classe contendo lógica de negócio no contexto de perfil."""

    def __init__(
        self, exercicio_dao: T_ExercicioDAO, usuario_dao: T_UsuarioDAO
    ) -> None:
        self.usuario_dao = usuario_dao
        self.exercicio_dao = exercicio_dao

    def listar_perfil(self, id_usuario: int) -> PerfilSchema:
        """Buscar perfil de um usuário"""

        perfil = self.usuario_dao.buscar_perfil_usuario(id_usuario)
        if not perfil:
            exc_msg = f"Perfil não encontrado para usuário {id_usuario}"
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc_msg)

        exs = self.exercicio_dao.listar_atividade(id_usuario)

        return converter_perfil_para_schema(perfil, exs)

    def atualizar_perfil(
        self,
        id_usuario: int,
        dados: AtualizarPerfilSchema,
        arquivo: UploadFile | str | None,
    ) -> MensagemSchema:
        """Atualizar informações do perfil de um usuário."""

        perfil = self.usuario_dao.buscar_perfil_usuario(id_usuario)
        if not perfil:
            exc_msg = f"Perfil não encontrado para usuário {id_usuario}"
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc_msg)

        caminho_local = None
        if arquivo and not isinstance(arquivo, str):
            caminho_local = salvar_imagem_perfil(arquivo)

        campos = self.usuario_dao.alterar_perfil_usuario(perfil, dados, caminho_local)
        s = "s" if len(campos) > 1 else ""
        msg = f"Os campo{s} {", ".join(campos)} foram alterados!"
        return MensagemSchema(mensagem=msg)

    def foto_perfil_usuario(self, id_usuario: int):
        """Buscar imagem do perfil do usuário."""

        perfil = self.usuario_dao.buscar_perfil_usuario(id_usuario)
        if not perfil:
            exc_msg = f"Perfil não encontrado para usuário {id_usuario}"
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=exc_msg)

        foto_url = perfil.url_img_perfil or "https://placehold.co/50x50"
        if foto_url.startswith("http"):
            return RedirectResponse(foto_url)

        caminho_local = Path(foto_url)
        if not caminho_local.exists():
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Imagem não encontrada"
            )

        return FileResponse(caminho_local)


def salvar_imagem_perfil(arquivo: UploadFile) -> str:
    """Salvar imagem no servidor."""

    if not arquivo or not arquivo.filename:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Nenhum arquivo enviado."
        )

    extensao = Path(arquivo.filename).suffix.lower()
    if extensao not in {".jpg", ".jpeg", ".png"}:
        raise HTTPException(
            status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
            detail="Formato de imagem não suportado. Use JPG ou PNG.",
        )

    nome_arquivo = f"{uuid.uuid4()}{extensao}"
    caminho_arquivo = PASTA_IMAGENS / nome_arquivo

    with caminho_arquivo.open("wb") as f:
        f.write(arquivo.file.read())

    return str(caminho_arquivo)


def converter_perfil_para_schema(perfil: Perfil, exs) -> PerfilSchema:
    """Converter o modelo do perfil para schema."""

    p = ProgressoSchema(
        qtd_sinais_aprendidos=perfil.qtd_ex_completos,
        nivel=perfil.nivel,
        pontos_total=perfil.pontos_total,
        pontos_nivel=perfil.pontos_nivel,
        pontos_para_subir=pontos_para_subir(perfil.nivel, perfil.pontos_nivel),
        msg_progresso=f"{calcular_porcentagem(perfil.nivel, perfil.pontos_nivel)}%",
    )

    a = []
    for ex in exs:
        sinal = ex["titulo"].replace("_", " ").title()
        data = ex["criado_em"]
        atividade = f"Realizou o sinal {sinal} com sucesso!"
        a.append((atividade, data))

    c = []
    for conq in perfil.conquistas:
        c.append(
            ConquistaSchema(
                id=conq.id, nome=conq.nome.value, descricao=conq.descricao or ""
            )
        )
        atividade = f"Conquista '{conq.nome.value}' obtida!"
        data = conq.data_conquista
        a.append((atividade, data))

    a.sort(key=lambda x: x[1], reverse=True)
    atividades = [
        AtividadeSchema(atividade=ati[0], data=ati[1].strftime("%d/%m/%Y %H:%M:%S"))
        for ati in a
    ]

    return PerfilSchema(
        nome_ou_apelido=perfil.apelido,
        imagem_fundo=perfil.url_img_fundo or "",
        imagem_perfil=f"/perfil/{perfil.id}/foto",
        aprendendo_desde=perfil.criado_em.strftime("%d/%m/%Y"),
        progresso=p,
        conquistas=c,
        atividade_recente=atividades,
    )
