import cv2

from facilibras.controladores.reconhecimento.frames import Camera
from facilibras.controladores.reconhecimento.mp_modelos import modelo_mao
from facilibras.controladores.reconhecimento.reconhecer import (
    extrair_pontos_mao,
    validar_sinal,
)
from facilibras.modelos.sinais import SinalLibras


def reconhecer_interativamente(sinal: SinalLibras):
    sinal.preparar_reconhecimento()
    frame_idx = 0

    with modelo_mao.Hands(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as modelo:
        for frame in Camera(0):
            # Pula frame
            frame_idx += 1
            if frame_idx % 3 != 0:
                continue

            # Processa frame
            frame = cv2.flip(frame, 1)
            imagem_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Extrai os pontos e valida
            pontos = extrair_pontos_mao(imagem_rgb, modelo)
            cor = (0, 0, 255)
            if pontos and validar_sinal(sinal, pontos, 0):
                cor = (0, 255, 0)

            # Exibe o o frame
            cv2.circle(frame, (50, 50), radius=25, color=cor, thickness=-1)
            cv2.imshow("Pressione q para sair", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
