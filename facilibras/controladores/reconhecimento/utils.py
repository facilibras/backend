import cv2
import numpy as np

from facilibras.controladores.reconhecimento.frames import GeradorFrames
from facilibras.controladores.reconhecimento.mp_modelos import modelo_mao
from facilibras.controladores.reconhecimento.validadores import Valido, get_validador
from facilibras.modelos.sinais import SinalLibras
from facilibras.modelos.sinais.base import Inclinacao, Orientacao


def exibir_resultado(*, resultado: bool) -> None:
    cor = (0, 255, 0) if resultado else (0, 0, 255)
    tela = np.full((500, 500, 3), cor, dtype=np.uint8)
    cv2.imshow("Tela", tela)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
