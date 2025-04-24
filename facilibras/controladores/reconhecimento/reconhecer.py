import time
from itertools import pairwise

import cv2

from facilibras.controladores.reconhecimento.frames import GeradorFrames
from facilibras.controladores.reconhecimento.mp_modelos import modelo_mao
from facilibras.controladores.reconhecimento.validadores import (
    Invalido,
    Valido,
    Validando,
    get_validador,
)
from facilibras.modelos.sinais import SinalLibras
from facilibras.modelos.sinais.base import Movimento, Tipo, Inclinacao, Orientacao


LIMIAR_CORRETO = 100
LIMIAR_INCORRETO = 100
DIAGONAIS = (
    Movimento.BAIXO_DIREITA,
    Movimento.BAIXO_ESQUERDA,
    Movimento.CIMA_DIREITA,
    Movimento.CIMA_ESQUERDA,
)
VERTICAL = (Movimento.CIMA, Movimento.BAIXO)
HORIZONTAIS = (Movimento.DIREITA, Movimento.ESQUERDA)
TEMPO_TOTAL = 5


def reconhecer_webcam(sinal: SinalLibras) -> bool:
    sinal.preparar_reconhecimento()

    match sinal.tipo:
        case Tipo.ESTATICO:
            res = reconhecer_estatico(sinal)
        case Tipo.COM_MOVIMENTO:
            res = reconhecer_com_movimento(sinal)
        case Tipo.COM_TRANSICAO:
            res = reconhecer_com_transicao(sinal)

    return res
    


def reconhecer_estatico(sinal: SinalLibras) -> bool:
    cap = cv2.VideoCapture(0)
    inicio = time.time()
    frame_idx = 0
    resultado = False

    while time.time() - inicio < TEMPO_TOTAL:
        ret, frame = cap.read()
        if not ret:
            break

        # Pula frame
        frame_idx += 1
        if frame_idx % 3 != 0:
            continue

        # Processa frame
        frame = cv2.flip(frame, 1)
        imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pontos = extrair_pontos_mao(imagem_rgb)

        # Extrai os pontos
        if pontos:
            resultado = validar_sinal(sinal, pontos, 0)

        cv2.imshow("Reconhecendo...", frame)
        if resultado or (cv2.waitKey(1) & 0xFF == ord("q")):
            break

    cap.release()
    cv2.destroyAllWindows()

    return resultado


def reconhecer_com_transicao(sinal: SinalLibras) -> bool:
    cap = cv2.VideoCapture(0)
    inicio = time.time()
    frame_idx = 0
    conf_idx = 0
    total_confs = len(sinal.confs)

    while time.time() - inicio < TEMPO_TOTAL:
        ret, frame = cap.read()
        if not ret:
            break

        # Pula frame
        frame_idx += 1
        if frame_idx % 3 != 0:
            continue

        # Processa frame
        frame = cv2.flip(frame, 1)
        imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Extrai os pontos
        pontos = extrair_pontos_mao(imagem_rgb)
        if pontos:
            resultado = validar_sinal(sinal, pontos, conf_idx)

            # Transição ocorreu
            if resultado:
                conf_idx += 1

        cv2.imshow("Reconhecendo...", frame)
        if conf_idx == total_confs or (cv2.waitKey(1) & 0xFF == ord("q")):
            break

    cap.release()
    cv2.destroyAllWindows()

    return conf_idx == total_confs


def reconhecer_com_movimento(sinal: SinalLibras):
    cap = cv2.VideoCapture(0)
    inicio = time.time()

    frames = []
    frame_idx = 0
    frames_bool = []

    while time.time() - inicio < TEMPO_TOTAL:
        ret, frame = cap.read()
        if not ret:
            break

        # Pula frame
        frame_idx += 1
        if frame_idx % 3 != 0:
            continue

        # Processa frame
        frame = cv2.flip(frame, 1)
        altura, largura, _ = frame.shape
        imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pontos = extrair_pontos_mao(imagem_rgb)
        if pontos:
            # Reconhece formato da mão
            reconheceu_formato = validar_sinal(sinal, pontos, 0)

            # Seta o frame com reconhecido ou não
            frames_bool.append(reconheceu_formato)
            x_px = int(pontos[8][0] * largura)
            y_px = int(pontos[8][1] * altura)
            frames.append((x_px, y_px, pontos[8][2]))

        cv2.imshow("Reconhecendo...", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Janela de frames consecutivos onde o formato da mão está correta
    frames_com_margem = adicionar_margem_de_erro(frames_bool, 3)
    janelas_continuas = validar_janelas_continuas(frames_com_margem, frames)

    # Por fim, avalia se houve movimento
    resultado = False
    for tentativa in janelas_continuas:
        resultado = reconhecer_sequencia_movimentos(
            posicoes=tentativa,
            movimentos=sinal.confs[0].movimentos,
            limiar_correto=100,
            limiar_incorreto=100,
        )
        if resultado:
            break

    return resultado


def reconhecer_sequencia_movimentos(
    posicoes: list[tuple[float, float, float]],
    movimentos: list[Movimento],
    limiar_correto: int = LIMIAR_CORRETO,
    limiar_incorreto: int = LIMIAR_INCORRETO,
    debug: bool = False,
) -> bool:
    # TODO: Refatorar essa função, tem repetição e redundância (pelo menos funciona)

    if not movimentos:
        raise ValueError("Deve haver pelo menos um movimento")

    if len(posicoes) <= len(movimentos):
        raise ValueError("Deve haver um frame a mais do que a quantidade de movimentos")

    anterior = None
    acumulado = (0, 0, 0)
    idx_mov_atual = 0
    ja_validado = False
    qtd_movimentos = len(movimentos)

    for pos1, pos2 in pairwise(posicoes):
        # Checa se terminou validação
        if idx_mov_atual == qtd_movimentos:
            return True

        # Verifica o movimento entre um par de frames
        validador_atual = get_validador(movimentos[idx_mov_atual])
        resultado = validador_atual(
            pos1, pos2, acumulado, limiar_correto, limiar_incorreto
        )

        if debug:
            print(
                f"DEBUG: ({idx_mov_atual}){movimentos[idx_mov_atual]}: {pos1} -> {pos2} + {acumulado} = {resultado}"
            )

        match resultado:
            case Valido():
                # Checa se validou todos os movimentos
                if idx_mov_atual + 1 == qtd_movimentos:
                    return True

                # Enquanto não ocorrer mudança de direção, continua validando
                # a mesma direção para permitir movimento a mais na mesma direção
                ja_validado = True

                # Considerar a possibilidade de manter a acumulação?
                acumulado = (0, 0, 0)

            case Invalido():
                # Se invalidar depois de já ter validado significa que ocorreu uma mudança de direção
                if ja_validado:
                    if debug:
                        print("DEBUG: Mudança de orientação (índice de movimentos++)")

                    # Avança para o próximo movimento
                    anterior = movimentos[idx_mov_atual]
                    idx_mov_atual += 1
                    if idx_mov_atual == qtd_movimentos:
                        return True

                    # No caso de anterior ser diagonal, reseta acumulativo
                    if anterior in DIAGONAIS:
                        if debug:
                            print("DEBUG: Reseta diagonal")
                        atual = movimentos[idx_mov_atual]
                        if atual in HORIZONTAIS:
                            acumulado = (0, acumulado[0], 0)
                        elif atual in VERTICAL:
                            acumulado = (acumulado[0], 0, 0)
                        else:
                            acumulado = (0, 0, 0)

                    # Checa se essa mudança de direção valida o próximo movimento
                    prox_validador = get_validador(movimentos[idx_mov_atual])
                    resultado = prox_validador(
                        pos1, pos2, acumulado, limiar_correto, limiar_incorreto
                    )

                    if debug:
                        debug_msg = "S" if resultado == Valido() else "Não s"
                        print(f"DEBUG: {debug_msg}uficiente para mudança")

                    match resultado:
                        case Valido():
                            if debug:
                                print(
                                    "DEBUG: Mudança de movimento correta (índice de movimentos++)"
                                )

                            # Movimento correto
                            if idx_mov_atual + 1 == qtd_movimentos:
                                return True

                            acumulado = (0, 0, 0)
                            continue  # Não reseta o ja_validado

                        case Invalido():
                            if debug:
                                print(
                                    f"DEBUG: Resetando (falha dentro do Valido) em {movimentos[idx_mov_atual]}"
                                )

                            # Mudança de movimento na direção errada -> reseta progresso
                            idx_mov_atual = 0
                            acumulado = (0, 0, 0)
                            anterior = None

                        case Validando(valor_acumulado):
                            if debug:
                                print(f"DEBUG: Novo valor acumulado {valor_acumulado}")

                            # Movimento não foi o suficiente, adiciona ele na próxima validação
                            acumulado = valor_acumulado

                # Falhou sem nunca ter validado
                else:
                    if debug:
                        print(
                            f"DEBUG: Resetando (falha Invalido) em {movimentos[idx_mov_atual]}"
                        )

                    # Movimento na direção errada -> reseta progresso
                    idx_mov_atual = 0
                    acumulado = (0, 0, 0)
                    anterior = None

                # Como invalidou, deve validar novamente para continuar movimento mesma direção
                ja_validado = False

            case Validando(valor_acumulado):
                if debug:
                    print(f"DEBUG: Novo valor acumulado {valor_acumulado}")

                # Movimento não foi o suficiente, adiciona ele na próxima validação
                acumulado = valor_acumulado

    return idx_mov_atual == qtd_movimentos


def extrair_pontos_mao(imagem_np) -> dict[int, tuple[float, float, float]]:
    resultados = modelo_mao.process(imagem_np)

    # Para o caso de não encontrar uma mão
    if not resultados.multi_hand_landmarks:
        return {}

    pontos = {}
    for hand_landmarks in resultados.multi_hand_landmarks:
        for i, landmark in enumerate(hand_landmarks.landmark):
            pontos[i] = (landmark.x, landmark.y, landmark.z)

    return pontos


def validar_sinal(
    sinal: SinalLibras, pontos: dict[int, tuple[float, float, float]], conf_idx: int
) -> bool:
    dedos = sinal.confs[conf_idx].dedos
    orientacao = sinal.confs[conf_idx].orientacao or Orientacao.FRENTE
    inclinacao = sinal.confs[conf_idx].inclinacao or Inclinacao.RETA

    return all(
        type(get_validador(dedo)(pontos, orientacao, inclinacao)) is Valido
        for dedo in dedos
    )


def validar_janelas_continuas(validos: list[bool], frames: list) -> list:
    janelas = []
    janela = []
    for i, fb in enumerate(validos):
        if fb:
            janela.append(frames[i])
        elif janela:
            janelas.append(janela)
            janela = []

    if janela:
        janelas.append(janela)

    return janelas


def adicionar_margem_de_erro(frames: list[bool], qtd: int = 3):
    n = qtd + 1
    copia = frames.copy()
    for i, valor in enumerate(copia):
        if valor:
            # Prox. N índices viram True, se existirem
            for j in range(i + 1, min(i + n, len(frames))):
                frames[j] = True

    return frames
