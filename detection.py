from cv2 import cv2 as cv
from threading import Thread, Lock

class Detection:

    # propiedades del thread
    stopped = True
    lock = None
    rectangles = []

    # propiedades
    cascade = None
    screenshot = None

    def __init__(self, model_file_path):
        # Crear un objeto lock
        self.lock = Lock()
        # Cargar el modelo entrenado
        self.cascade = cv.CascadeClassifier(model_file_path)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                rectangles = self.cascade.detectMultiScale(self.screenshot)
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()