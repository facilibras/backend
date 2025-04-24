# from facilibras.modelos.sinais.base import Inclinacao, Orientacao
import cv2
import mediapipe as mp

# from facilibras.modelos.sinais import SinalLibras
from facilibras.controladores.reconhecimento.frames import GeradorFrames
from facilibras.controladores.reconhecimento.mp_modelos import modelo_mao


def processar_gestos(frames: GeradorFrames):
    with modelo_mao.Hands(
        max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5
    ) as hands:
        for frame in frames:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                for lm in results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(  # type: ignore
                        frame, lm, modelo_mao.HAND_CONNECTIONS
                    )

            cv2.imshow("MediaPipe Hands", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cv2.destroyAllWindows()
