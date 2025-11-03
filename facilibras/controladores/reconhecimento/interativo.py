from contextlib import nullcontext

import cv2

from facilibras.controladores.reconhecimento.frames import Camera
from facilibras.controladores.reconhecimento.mp_modelos import (
    modelo_corpo,
    modelo_mao,
    modelo_rosto,
)
from facilibras.controladores.reconhecimento.reconhecer import (
    extrair_pontos_corpo,
    extrair_pontos_mao,
    identificar_mao,
    montar_feedback,
    validar_mao,
    validar_posicao,
)
from facilibras.modelos.sinais import SinalLibras
from facilibras.schemas.exercicios import Feedback


def reconhecer_interativamente(sinal: SinalLibras) -> bool:
    sinal.preparar_reconhecimento()
    frame_idx = 0
    reconheceu = False
    pos_anterior = (-1, -1, -1)
    modelo_rosto_contexto = (
        modelo_rosto.FaceMesh() if sinal.possui_expressao_facial else nullcontext()
    )

    with (
        modelo_mao.Hands(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        ) as mm,
        modelo_corpo.Pose() as mc,
        modelo_rosto_contexto as _,
    ):
        for frame in Camera(0, 30):
            # Pula frame
            frame_idx += 1
            if frame_idx % 3 != 0:
                continue

            # Processa frame
            frame = cv2.flip(frame, 1)
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extrai os pontos e valida
            pontos = extrair_pontos_mao(imagem_rgb, mm)
            pontos_corpo = extrair_pontos_corpo(imagem_rgb, mc)

            cor = (0, 0, 255)
            msg = ""
            if pontos and pontos_corpo:
                # Mao
                mao = identificar_mao(pontos, pontos_corpo)
                resultado_mao, erros_mao = validar_mao(sinal, pontos, 0)
                e = [[False, erro] for erro in erros_mao]
                msg = montar_feedback(resultado_mao, e)

                # Corpo
                pos_dedo = pontos[sinal.confs[0].ponto_ref]
                resultado_posicao, feed_pos = validar_posicao(
                    sinal, pos_dedo, pos_anterior, pontos_corpo, 0, mao
                )
                if not resultado_posicao:
                    msg.feedback.append(
                        Feedback(
                            correto=resultado_posicao,
                            mensagem=feed_pos.replace("ç", "c").replace("ã", "a"),
                        )
                    )

                # Res final
                resultado = resultado_mao and resultado_posicao
                if resultado:
                    cor = (0, 255, 0)
                    reconheceu = True

            # Exibe o o frame
            if msg:
                y_base = 100
                incremento = 20
                for i, feed in enumerate(msg.feedback):
                    y = y_base + i * incremento

                    cv2.putText(
                        frame,
                        feed.mensagem,
                        (30, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0),
                        1,
                        cv2.LINE_AA,
                    )

            cv2.circle(frame, (50, 50), radius=25, color=cor, thickness=-1)
            cv2.imshow("Pressione q para sair", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
    return reconheceu
