import time
from abc import ABC, abstractmethod
from enum import Enum

import cv2


class TipoGerador(Enum):
    CAMERA = 1
    VIDEO = 2
    OUTRO = 3


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

    @property
    @abstractmethod
    def tipo(self) -> TipoGerador: ...

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
    def __init__(self, index=0, timeout=5):
        super().__init__()
        self.index = index
        self.timeout = timeout

    def open(self):
        self.cap = cv2.VideoCapture(self.index)

    @property
    def tipo(self) -> TipoGerador:
        return TipoGerador.CAMERA

    def __iter__(self):
        """Iterador que vai retornando frames até a fonte acabar."""
        self.open()
        inicio = None

        while True:
            ret, frame = self.cap.read()  # type: ignore
            if not ret:
                break

            if inicio is None:
                inicio = time.time()

            if time.time() - inicio > self.timeout:
                break

            yield frame

        self.release()


class Video(GeradorFrames):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def open(self):
        self.cap = cv2.VideoCapture(self.path)

    @property
    def tipo(self) -> TipoGerador:
        return TipoGerador.VIDEO
