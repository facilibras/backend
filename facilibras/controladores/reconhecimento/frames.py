from abc import ABC, abstractmethod

import cv2


class GeradorFrames(ABC):
    """Interface genérica para qualquer fonte de frames."""

    def __init__(self):
        self.cap = None

    @abstractmethod
    def open(self):
        """Inicializa self.cap (cv2.VideoCapture)."""
        ...

    def release(self):
        """Libera o capture."""
        if self.cap:
            self.cap.release()

    def __iter__(self):
        """Iterador que vai retornando frames até a fonte acabar."""
        self.open()
        while True:
            ret, frame = self.cap.read()  # type: ignore
            if not ret:
                break
            yield frame
        self.release()


class Camera(GeradorFrames):
    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def open(self):
        self.cap = cv2.VideoCapture(self.index)


class Video(GeradorFrames):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def open(self):
        self.cap = cv2.VideoCapture(self.path)
