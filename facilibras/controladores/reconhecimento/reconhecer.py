import time
from itertools import pairwise

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
    Validando,
    Valido,
    get_validador,
)
from facilibras.modelos.sinais import SinalLibras
from facilibras.modelos.sinais.base import Inclinacao, Movimento, Orientacao, Tipo

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


def reconhecer_webcam(sinal: SinalLibras) -> tuple[bool, str]:
    return reconhecer(sinal, Camera(0))


def reconhecer_video(sinal: SinalLibras, caminho_video: str) -> tuple[bool, str]:
    return reconhecer(sinal, Video(caminho_video))


def reconhecer(sinal: SinalLibras, gerador: GeradorFrames) -> tuple[bool, str]:
    sinal.preparar_reconhecimento()

    match sinal.tipo:
        case Tipo.ESTATICO:
            res, erros = reconhecer_estatico(sinal, gerador, TEMPO_TOTAL)
        case Tipo.COM_MOVIMENTO:
            res, erros = reconhecer_com_movimento(sinal, gerador, TEMPO_TOTAL)
        case Tipo.COM_TRANSICAO:
            res, erros = reconhecer_com_transicao(sinal, gerador, TEMPO_TOTAL)

    return res, montar_feedback(erros)


def reconhecer_estatico(
    sinal: SinalLibras, gerador: GeradorFrames, tempo_limite: int
) -> tuple[bool, list[str]]:
    inicio = time.time()
    frame_idx = 0
    resultado = False
    melhor = float("inf")
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
            pontos = extrair_pontos_mao(imagem_rgb, modelo)

            # Valida sinal
            if pontos:
                resultado, erros = validar_sinal(sinal, pontos, 0)
                qtd_erros = len(erros)
                if qtd_erros <= melhor:
                    melhor = qtd_erros
                    feedback = erros

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
) -> tuple[bool, list[str]]:
    inicio = time.time()
    frame_idx = 0
    conf_idx = 0
    total_confs = len(sinal.confs)
    melhor = float("inf")
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
                resultado, erros = validar_sinal(sinal, pontos, conf_idx)
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
        return True, []
    if not feedback:
        return False, ["Faltou movimento"]
    return False, [
        *feedback,
        "Corrija a configuração da mão antes de fazer o movimento",
    ]


def reconhecer_com_movimento(
    sinal: SinalLibras, gerador: GeradorFrames, tempo_limite: int
):
    inicio = time.time()
    frames = []
    frame_idx = 0
    frames_bool = []
    melhor = float("inf")
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
            altura, largura, _ = frame.shape
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            pontos = extrair_pontos_mao(imagem_rgb, modelo)
            if pontos:
                # Reconhece formato da mão
                reconheceu_formato, erros = validar_sinal(sinal, pontos, 0)
                qtd_erros = len(erros)
                if qtd_erros <= melhor:
                    melhor = qtd_erros
                    feedback = erros

                # Seta o frame com reconhecido ou não
                frames_bool.append(reconheceu_formato)
                x_px = int(pontos[8][0] * largura)
                y_px = int(pontos[8][1] * altura)
                frames.append((x_px, y_px, pontos[8][2]))

            atingiu_tempo = time.time() - inicio >= tempo_limite
            if gerador.tipo == TipoGerador.CAMERA:
                cv2.imshow("Reconhecendo...", frame)
                if (cv2.waitKey(1) & 0xFF == ord("q")) or atingiu_tempo:
                    break
            elif atingiu_tempo:
                break

    cv2.destroyAllWindows()

    # Janela de frames consecutivos onde o formato da mão está correta
    frames_com_margem = adicionar_margem_de_erro(frames_bool, 3)
    janelas_continuas = validar_janelas_continuas(frames_com_margem, frames)

    # Por fim, avalia se houve movimento
    if not janelas_continuas:
        return False, feedback

    resultado = False
    teve_movimento = False
    for tentativa in janelas_continuas:
        resultado = reconhecer_sequencia_movimentos(
            posicoes=tentativa,
            movimentos=sinal.confs[0].movimentos,
            limiar_correto=100,
            limiar_incorreto=100,
        )
        if resultado:
            teve_movimento = True
            break

    if not teve_movimento:
        return resultado, ["Faltou movimento"]
    return resultado, feedback


def reconhecer_sequencia_movimentos(
    posicoes: list[tuple[float, float, float]],
    movimentos: list[Movimento],
    limiar_correto: int = LIMIAR_CORRETO,
    limiar_incorreto: int = LIMIAR_INCORRETO,
    debug: bool = False,
) -> bool:
    # TODO: Refatorar essa função, tem repetição e redundância (pelo menos funciona)

    if not movimentos:
        exc = "Deve haver pelo menos um movimento"
        raise ValueError(exc)

    if len(posicoes) <= len(movimentos):
        exc = "Deve haver um frame a mais do que a quantidade de movimentos"
        raise ValueError(exc)

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
            pos_str = f"{pos1} -> {pos2} + {acumulado} = {resultado}"
            print(f"DEBUG: ({idx_mov_atual}){movimentos[idx_mov_atual]}: {pos_str}")

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
                # Se invalidar depois de já ter validado, ocorreu mudança de direção
                if ja_validado:
                    if debug:
                        print("DEBUG: Mudança de orientação (ídx mov++)")

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
                                print("DEBUG: Mudança de movimento correta (ídx mov++)")

                            # Movimento correto
                            if idx_mov_atual + 1 == qtd_movimentos:
                                return True

                            acumulado = (0, 0, 0)
                            continue  # Não reseta o ja_validado

                        case Invalido():
                            if debug:
                                print(
                                    f"DEBUG: Resetando em {movimentos[idx_mov_atual]}"
                                )

                            # Mudança de movimento na dir errada -> reseta progresso
                            idx_mov_atual = 0
                            acumulado = (0, 0, 0)
                            anterior = None

                        case Validando(valor_acumulado):
                            if debug:
                                print(f"DEBUG: Novo valor acumulado {valor_acumulado}")

                            # Movimento não suficiente, adiciona na próxima validação
                            acumulado = valor_acumulado

                # Falhou sem nunca ter validado
                else:
                    if debug:
                        print(f"DEBUG: Resetando em {movimentos[idx_mov_atual]}")

                    # Movimento na direção errada -> reseta progresso
                    idx_mov_atual = 0
                    acumulado = (0, 0, 0)
                    anterior = None

                # Como invalidou, valida novamente p/ continuar movimento mesma direção
                ja_validado = False

            case Validando(valor_acumulado):
                if debug:
                    print(f"DEBUG: Novo valor acumulado {valor_acumulado}")

                # Movimento não foi o suficiente, adiciona ele na próxima validação
                acumulado = valor_acumulado

    return idx_mov_atual == qtd_movimentos


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


def montar_feedback(mensagens: list[str]) -> str:
    feedback = ", ".join([f"{i + 1}: {msg}" for i, msg in enumerate(mensagens)])
    return feedback


def validar_sinal(
    sinal: SinalLibras, pontos: dict[int, tuple[float, float, float]], conf_idx: int
) -> tuple[bool, list[str]]:
    dedos = sinal.confs[conf_idx].dedos
    orientacao = sinal.confs[conf_idx].orientacao or Orientacao.FRENTE
    inclinacao = sinal.confs[conf_idx].inclinacao or Inclinacao.RETA

    validadores = [get_validador(dedo) for dedo in dedos]
    sucesso = True
    mensagens = []

    for validador in validadores:
        resultado = validador(pontos, orientacao, inclinacao)
        if type(resultado) is Invalido:
            sucesso = False
            mensagens.append(resultado.mensagem)

    return sucesso, mensagens


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
