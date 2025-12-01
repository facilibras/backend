import time
from contextlib import nullcontext

import cv2

from facilibras.controladores.reconhecimento.frames import (
    Camera,
    GeradorFrames,
    TipoGerador,
    Video,
)
from facilibras.controladores.reconhecimento.mp_modelos import (
    modelo_corpo,
    modelo_mao,
    modelo_rosto,
)
from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    get_validador,
)
from facilibras.controladores.reconhecimento.validadores.utils import distancia2
from facilibras.modelos.mao import Mao
from facilibras.modelos.sinais import SinalLibras, Tipo
from facilibras.schemas import Feedback, FeedbackSchema

# constantes
TEMPO_TOTAL = 5
MAXIMO_ERRADO = 50

# feedback
INCORRETA = "Incorreta"
CORRETA = "Correta"
TAB = "   "
F_MAO = TAB + "Configuração da mão: "
F_POS = TAB + "Posição da mão: "
F_EXP = TAB + "Expressão facial: "


def reconhecer_webcam(sinal: SinalLibras) -> FeedbackSchema:
    return reconhecer(sinal, Camera(0))


def reconhecer_video(sinal: SinalLibras, caminho_video: str) -> FeedbackSchema:
    return reconhecer(sinal, Video(caminho_video))


def reconhecer(sinal: SinalLibras, gerador: GeradorFrames) -> FeedbackSchema:
    sinal.preparar_reconhecimento()

    match sinal.tipo:
        case Tipo.UMA_MAO:
            res, erros = reconhecer_com_transicao(sinal, gerador, TEMPO_TOTAL)
        case Tipo.DUAS_MAOS:
            res, erros = reconhecer_duas_maos(sinal, gerador, TEMPO_TOTAL)

    return montar_feedback(res, erros)


def reconhecer_com_transicao(
    sinal: SinalLibras, gerador: GeradorFrames, tempo_limite: int
) -> tuple[bool, list[list]]:
    inicio = time.time()
    frame_idx = 0
    conf_idx = 0
    pos_anterior = (0, 0, 0)
    ultimo_correto = 0
    total_confs = len(sinal.confs)
    melhor = [float("inf")] * total_confs
    feedback = [[] for _ in range(total_confs)]

    contexto_rosto = (
        modelo_rosto.FaceMesh() if sinal.possui_expressao_facial else nullcontext()
    )

    with modelo_mao.Hands() as mm, modelo_corpo.Pose() as mc, contexto_rosto as mr:
        for frame in gerador:
            # Pula frame
            frame_idx += 1
            if frame_idx % 3 != 0:
                continue

            # Processa frame
            frame = cv2.flip(frame, 1)
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extrai pontos
            pontos_mao = extrair_pontos_mao(imagem_rgb, mm)
            pontos_corpo = extrair_pontos_corpo(imagem_rgb, mc)

            if pontos_mao and pontos_corpo:
                # Identifica mão e dedo
                mao = identificar_mao(pontos_mao, pontos_corpo)
                pos_dedo = pontos_mao[sinal.confs[conf_idx].ponto_ref]

                # Valida essencial
                res_mao, erros = validar_mao(sinal, pontos_mao, conf_idx, mao)
                res_posicao, feedback_posicao = validar_posicao(
                    sinal, pos_dedo, pos_anterior, pontos_corpo, conf_idx, mao
                )

                resultado = res_mao and res_posicao
                pos_anterior = pos_dedo
                if not res_posicao:
                    erros.append(feedback_posicao)

                # Valida rosto (se necessãrio)
                if sinal.confs[conf_idx].possui_expressao_facial:
                    pontos_rosto = extrair_pontos_rosto(imagem_rgb, mr)
                    res_rosto, feedback_rosto = validar_rosto(
                        sinal, pontos_rosto, conf_idx
                    )
                    resultado = resultado and res_rosto
                    if not res_rosto:
                        erros.append(feedback_rosto)

                # Checa se deve atualizar feedback
                qtd_erros = len(erros)
                if qtd_erros <= melhor[conf_idx]:
                    melhor[conf_idx] = qtd_erros
                    feedback[conf_idx] = []

                    # Feedback mão
                    if res_mao:
                        feedback[conf_idx].append([True, F_MAO + CORRETA])
                    else:
                        feedback[conf_idx].append([False, F_MAO + INCORRETA])
                        if sinal.simples:
                            for erro in erros:
                                feedback[conf_idx].append([False, TAB + erro])

                    # Feedback posição
                    if sinal.confs[conf_idx].possui_posicao:
                        if res_posicao:
                            feedback[conf_idx].append([True, F_POS + CORRETA])
                        else:
                            feedback[conf_idx].append([False, F_POS + INCORRETA])

                    # Feedback expressão facial
                    if sinal.confs[conf_idx].possui_expressao_facial:
                        if res_rosto:
                            feedback[conf_idx].append([True, F_EXP + CORRETA])
                        else:
                            feedback[conf_idx].append([False, F_EXP + INCORRETA])

                # Transição ocorreu
                if resultado:
                    conf_idx += 1
                    ultimo_correto = frame_idx

                # Não ocorreu dentro de um determinado intervalo
                elif frame_idx - ultimo_correto > MAXIMO_ERRADO:
                    conf_idx = 0

            # Lógica exclusiva do reconhecimento por webcam
            atingiu_tempo = time.time() - inicio >= tempo_limite
            if gerador.tipo == TipoGerador.CAMERA:
                cv2.imshow("Reconhecendo...", frame)
                if (
                    conf_idx == total_confs
                    or (cv2.waitKey(1) & 0xFF == ord("q"))
                    or atingiu_tempo
                ):
                    break

            # Se deve ou não encerrar o reconhecimento
            elif conf_idx == total_confs or atingiu_tempo:
                break

    cv2.destroyAllWindows()

    sucesso = conf_idx == total_confs
    feedback_final = []

    if sucesso:
        for idx, conf in enumerate(sinal.confs):
            feedback_final.append([True, f"{idx+1}: " + conf.descricao])
            feedback_final.append([True, F_MAO + CORRETA])

            if conf.possui_posicao:
                feedback_final.append([True, F_POS + CORRETA])

            if conf.possui_expressao_facial:
                feedback_final.append([True, F_EXP + CORRETA])

        return True, feedback_final

    for idx, feed_conf in enumerate(feedback):
        msg = f"{idx+1}: " + sinal.confs[idx].descricao
        print(feed_conf)

        if melhor[idx] == 0:
            feedback_final.append([True, msg])
        else:
            feedback_final.append([False, msg])
            feedback_final.extend(feed_conf)

    return False, feedback_final


def reconhecer_duas_maos(
    sinal: SinalLibras, gerador: GeradorFrames, tempo_limite: int
) -> tuple[bool, list[list]]:
    inicio = time.time()
    frame_idx = 0
    conf_idx = 0
    pos_anterior = (0, 0, 0)
    total_confs = len(sinal.confs)

    with modelo_mao.Hands() as mm, modelo_corpo.Pose() as mc:
        for frame in gerador:
            # Pula frame
            frame_idx += 1
            if frame_idx % 3 != 0:
                continue

            # Processa frame
            frame = cv2.flip(frame, 1)
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extrai pontos
            pontos_esq, pontos_dir = extrair_pontos_duas_maos(imagem_rgb, mm)
            pontos_corpo = extrair_pontos_corpo(imagem_rgb, mc)

            if pontos_esq and pontos_dir and pontos_corpo:
                # Extrai ponto de referência para cada mão
                pos_dedo_esq = pontos_esq[sinal.confs[conf_idx].ponto_ref]
                pos_dedo_dir = pontos_dir[sinal.confs[conf_idx + 1].ponto_ref]

                # Valida mão esquerda/direita
                res_esq, _ = validar_mao(sinal, pontos_esq, conf_idx, Mao.ESQUERDA)
                res_dir, _ = validar_mao(sinal, pontos_dir, conf_idx + 1, Mao.DIREITA)

                # Valida posição das mãos
                res_pos_esq, _ = validar_posicao(
                    sinal,
                    pos_dedo_esq,
                    pos_anterior,
                    pontos_corpo,
                    conf_idx,
                    Mao.ESQUERDA,
                )
                res_pos_dir, _ = validar_posicao(
                    sinal,
                    pos_dedo_dir,
                    pos_anterior,
                    pontos_corpo,
                    conf_idx + 1,
                    Mao.DIREITA,
                )

                res_mao = res_esq and res_dir
                res_posicao = res_pos_esq and res_pos_dir
                resultado = res_mao and res_posicao

                # Transição ocorreu
                if resultado:
                    conf_idx += 2

            # Lógica exclusiva do reconhecimento por webcam
            atingiu_tempo = time.time() - inicio >= tempo_limite
            if gerador.tipo == TipoGerador.CAMERA:
                cv2.imshow("Reconhecendo...", frame)
                if (
                    conf_idx == total_confs
                    or (cv2.waitKey(1) & 0xFF == ord("q"))
                    or atingiu_tempo
                ):
                    break

            # Se deve ou não encerrar o reconhecimento
            elif conf_idx >= total_confs or atingiu_tempo:
                break

    cv2.destroyAllWindows()

    sucesso = conf_idx == total_confs
    feedback_final = []

    if sucesso:
        for conf in sinal.confs:
            feedback_final.append([True, conf.descricao])  # noqa: PERF401

        return True, feedback_final

    passo = 0
    for idx in range(total_confs):
        if idx % 2 == 0:
            passo += 1
            sucesso = idx < conf_idx
            feedback_final.append([sucesso, f"{passo} - Simultaneamente faça:"])
            feedback_final.append([sucesso, sinal.confs[idx].descricao])
        else:
            feedback_final.append([sucesso, sinal.confs[idx].descricao])

    return False, feedback_final


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


def extrair_pontos_duas_maos(imagem_np, modelo):
    resultados = modelo.process(imagem_np)

    if not resultados.multi_hand_landmarks:
        return {}, {}

    maos_detectadas = []
    for hand_landmarks in resultados.multi_hand_landmarks:
        pontos = {i: (lm.x, lm.y, lm.z) for i, lm in enumerate(hand_landmarks.landmark)}
        x_pulso = hand_landmarks.landmark[0].x
        maos_detectadas.append((x_pulso, pontos))

    maos_detectadas.sort(key=lambda m: m[0])
    esquerda, direita = {}, {}

    if len(maos_detectadas) == 2:
        esquerda = maos_detectadas[0][1]
        direita = maos_detectadas[1][1]

    return esquerda, direita


def extrair_pontos_corpo(imagem, modelo) -> dict[int, tuple[float, float, float]]:
    resultado = modelo.process(imagem)

    # Para o caso de não encontrar um corpo
    if not resultado.pose_landmarks:
        return {}

    pontos = {}
    for i, landmark in enumerate(resultado.pose_landmarks.landmark):
        pontos[i] = (landmark.x, landmark.y, landmark.z)

    return pontos


def extrair_pontos_rosto(imagem, modelo) -> dict[int, tuple[float, float, float]]:
    resultado = modelo.process(imagem)

    # Para o caso de não encontrar nenhum rosto
    if not resultado.multi_face_landmarks:
        return {}

    rosto = resultado.multi_face_landmarks[0]

    pontos = {}
    for i, landmark in enumerate(rosto.landmark):
        pontos[i] = (landmark.x, landmark.y, landmark.z)

    return pontos


def montar_feedback(sucesso: bool, feedbacks: list[list]) -> FeedbackSchema:
    fs = FeedbackSchema(sucesso=sucesso)
    for correto, mensagem in feedbacks:
        fs.feedback.append(Feedback(correto=correto, mensagem=mensagem))

    return fs


def identificar_mao(mao, corpo) -> Mao:
    from facilibras.config.env import get_variavel_ambiente_atual

    if get_variavel_ambiente_atual("SOMENTE_DIREITA", int, 0):
        identificada = Mao.DIREITA
    else:
        identificada = identificar_pela_pose(mao, corpo)

    return identificada


def identificar_pela_pose(pontos_mao: dict, pontos_corpo: dict) -> Mao:
    if not pontos_mao or not pontos_corpo:
        return Mao.DIREITA  # não importa pois vai ser ignorado

    # pulso da mão detectada
    pulso_detectado = pontos_mao[0]
    pulso_esq = 15
    pulso_dir = 16

    # se algum desses índices não existe na pose, assume direita
    if pulso_esq not in pontos_corpo or pulso_dir not in pontos_corpo:
        return Mao.DIREITA

    # ve qual mão está mais próxima do pulso
    dist_esq = distancia2(pulso_detectado, pontos_corpo[pulso_esq])
    dist_dir = distancia2(pulso_detectado, pontos_corpo[pulso_dir])

    # Invertido pq o frame foi espelhado
    if dist_esq < dist_dir:
        return Mao.DIREITA
    return Mao.ESQUERDA


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


def validar_rosto(
    sinal: SinalLibras,
    pontos: dict[int, tuple[float, float, float]],
    conf_idx: int,
) -> tuple[bool, str]:
    validador = get_validador(sinal.confs[conf_idx].expressao)
    resultado = validador(pontos)

    sucesso = True
    mensagem = "Expressão facial correta"
    if type(resultado) is Invalido:
        sucesso = False
        mensagem = resultado.mensagem

    return sucesso, mensagem
