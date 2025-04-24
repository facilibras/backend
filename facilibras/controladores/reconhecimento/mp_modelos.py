import mediapipe as mp

mp_hands = mp.solutions.hands  # type: ignore
modelo_mao = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
