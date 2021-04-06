import numpy as np
import win32gui, win32ui, win32con
from threading import Thread, Lock

class WindowCapture:

    # propiedades del thread
    stopped = True
    lock = None
    screenshot = None

    # Propiedades
    width = 0
    height = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # Constructor
    def __init__(self, window_name = None):

        # Creamos un hilo del objeto lock
        self.lock = Lock()

        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Ventana no encontrada: '.format(window_name))
        

        # Cogemos el tamaño de la pantalla
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]


        # Retiramos el borde negro de la ventana
        border_pixels = 8
        titlebar_pixels = 30
        self.width = self.width - (border_pixels * 2)
        self.height = self.height - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # Setteamos las cordenadas para que podamos trasladar las fotos a la posicion de la pantalla
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        # Cogemos los datos de la imagen
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.width, self.height), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # Convertimos los datos en un formato que pueda leer opencv
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img
    
    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # trasladamos la posicion de pixel de captura de pantalla a la posicion de la pantalla
    # AVISO: SI MUEVES LA PANTALLA UNA VEZ SE ESTA EJECUTANDO VA A DEVOLVER MAL LAS COORDENADAS EN EL INIT
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    # hilo

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            # obtener una imagen actualizada del juego
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()