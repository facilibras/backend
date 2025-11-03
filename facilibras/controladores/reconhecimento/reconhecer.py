import time

import cv2

from facilibras.controladores.reconhecimento.frames import (
    Camera,
    GeradorFrames,
    TipoGerador,
    Video,
)
from facilibras.controladores.reconhecimento.mp_modelos import modelo_mao
from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    get_validador,
)
from facilibras.modelos.mao import Mao
from facilibras.modelos.sinais import SinalLibras
from facilibras.modelos.sinais.base import Inclinacao, Orientacao, Tipo
from facilibras.schemas import Feedback, FeedbackSchema

TEMPO_TOTAL = 5


def reconhecer_webcam(sinal: SinalLibras) -> FeedbackSchema:
    return reconhecer(sinal, Camera(0))


def reconhecer_video(sinal: SinalLibras, caminho_video: str) -> FeedbackSchema:
    return reconhecer(sinal, Video(caminho_video))


def reconhecer(sinal: SinalLibras, gerador: GeradorFrames) -> FeedbackSchema:
    sinal.preparar_reconhecimento()

    match sinal.tipo:
        case Tipo.ESTATICO:
            res, erros = reconhecer_estatico(sinal, gerador, TEMPO_TOTAL)
        case Tipo.COM_TRANSICAO:
            res, erros = reconhecer_com_transicao(sinal, gerador, TEMPO_TOTAL)

    return montar_feedback(res, erros)


def reconhecer_estatico(
    sinal: SinalLibras, gerador: GeradorFrames, tempo_limite: int
) -> tuple[bool, list[list]]:
    inicio = time.time()
    frame_idx = 0
    resultado = False
    melhor = float("inf")
    feedback = [[False, ""]]

    with modelo_mao.Hands(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as modelo:
        for frame in gerador:
            # Pula frame
            frame_idx += 1
            if frame_idx % 3 != 0:
                continue

            # Processa frame
            frame = cv2.flip(frame, 1)
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pontos = extrair_pontos_mao(imagem_rgb, modelo)

            # Valida sinal
            if pontos:
                resultado, erros = validar_mao(sinal, pontos, 0)
                qtd_erros = len(erros)
                if qtd_erros <= melhor:
                    melhor = qtd_erros
                    feedback[0] = [False, "/".join(erros)]
                if resultado:
                    feedback[0] = [True, "Configuração da mão correta"]

            atingiu_tempo = time.time() - inicio >= tempo_limite
            if gerador.tipo == TipoGerador.CAMERA:
                cv2.imshow("Reconhecendo...", frame)
                if resultado or (cv2.waitKey(1) & 0xFF == ord("q")) or atingiu_tempo:
                    break
            elif resultado or atingiu_tempo:
                break

    cv2.destroyAllWindows()

    return resultado, feedback


def reconhecer_com_transicao(
    sinal: SinalLibras, gerador: GeradorFrames, tempo_limite: int
) -> tuple[bool, list[list]]:
    inicio = time.time()
    frame_idx = 0
    conf_idx = 0
    total_confs = len(sinal.confs)
    melhor = float("inf")
    # feedback = [[False, ""] for _ in range(total_confs)]
    feedback = []

    with modelo_mao.Hands(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as modelo:
        for frame in gerador:
            # Pula frame
            frame_idx += 1
            if frame_idx % 3 != 0:
                continue

            # Processa frame
            frame = cv2.flip(frame, 1)
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extrai os pontos
            pontos = extrair_pontos_mao(imagem_rgb, modelo)
            if pontos:
                resultado, erros = validar_mao(sinal, pontos, conf_idx)
                qtd_erros = len(erros)
                if qtd_erros <= melhor:
                    melhor = qtd_erros
                    feedback = erros

                # Transição ocorreu
                if resultado:
                    conf_idx += 1

            atingiu_tempo = time.time() - inicio >= tempo_limite
            if gerador.tipo == TipoGerador.CAMERA:
                cv2.imshow("Reconhecendo...", frame)
                if (
                    conf_idx == total_confs
                    or (cv2.waitKey(1) & 0xFF == ord("q"))
                    or atingiu_tempo
                ):
                    break
            elif conf_idx == total_confs or atingiu_tempo:
                break

    cv2.destroyAllWindows()

    sucesso = conf_idx == total_confs
    if sucesso:
        return True, [
            [True, "Configuração da mão: Correto"],
            [True, "Movimento: Correto"],
        ]
    if not feedback:
        return False, [
            [True, "Configuração da mão: Correto"],
            [False, "Movimento: Incorreto ou não detectado."],
        ]
    return False, [
        [False, "Configuração da mão: Incorreta (" + "/".join(feedback) + ")"],
        [False, "Movimento: Corrija a configuração da mão antes de fazer o movimento"],
    ]


def extrair_pontos_mao(imagem_np, modelo) -> dict[int, tuple[float, float, float]]:
    resultados = modelo.process(imagem_np)

    # Para o caso de não encontrar uma mão
    if not resultados.multi_hand_landmarks:
        return {}

    pontos = {}
    for hand_landmarks in resultados.multi_hand_landmarks:
        for i, landmark in enumerate(hand_landmarks.landmark):
            pontos[i] = (landmark.x, landmark.y, landmark.z)

    return pontos


def extrair_pontos_corpo(imagem, modelo) -> dict[int, tuple[float, float, float]]:
    resultado = modelo.process(imagem)

    # Para o caso de não encontrar um corpo
    if not resultado.pose_landmarks:
        return {}

    pontos = {}
    for i, landmark in enumerate(resultado.pose_landmarks.landmark):
        pontos[i] = (landmark.x, landmark.y, landmark.z)

    return pontos


def montar_feedback(sucesso: bool, feedbacks: list[list]) -> FeedbackSchema:
    fs = FeedbackSchema(sucesso=sucesso)
    for correto, mensagem in feedbacks:
        fs.feedback.append(Feedback(correto=correto, mensagem=mensagem))

    return fs


def validar_mao(
    sinal: SinalLibras,
    pontos: dict[int, tuple[float, float, float]],
    conf_idx: int,
    mao: Mao = Mao.DIREITA,
) -> tuple[bool, list[str]]:
    dedos = sinal.confs[conf_idx].dedos
    orientacao = sinal.confs[conf_idx].orientacao
    inclinacao = sinal.confs[conf_idx].inclinacao

    validadores = [get_validador(dedo) for dedo in dedos]
    sucesso = True
    mensagens = []

    for validador in validadores:
        resultado = validador(pontos, orientacao, inclinacao, mao)
        if type(resultado) is Invalido:
            sucesso = False
            mensagens.append(resultado.mensagem)

    return sucesso, mensagens


def validar_posicao(
    sinal: SinalLibras,
    pos_dedo: tuple[float, float, float],
    pos_anterior: tuple[float, float, float],
    pontos_corpo: dict[int, tuple[float, float, float]],
    conf_idx: int,
    mao: Mao,
) -> tuple[bool, str]:
    validador = get_validador(sinal.confs[conf_idx].posicao)
    resultado = validador(pos_dedo, pos_anterior, pontos_corpo, mao)

    sucesso = True
    mensagem = "Posição correta"
    if type(resultado) is Invalido:
        sucesso = False
        mensagem = resultado.mensagem

    return sucesso, mensagem


def identificar_mao(corpo, mao) -> Mao:
    return Mao.DIREITA
