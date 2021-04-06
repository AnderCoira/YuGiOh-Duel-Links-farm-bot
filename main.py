from cv2 import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowCapture import WindowCapture
from trainers import Trainers
from detection import Detection
import win32gui, win32ui, win32con, win32api


DEBUG = True

# Instancias
window_capture = WindowCapture('Yu-Gi-Oh! DUEL LINKS')
detector = Detection('cascade/cascade.xml')
trainers = Trainers()

# Empezar los procesos
window_capture.start()
detector.start()


while(True):

    # screenshot = window_capture()
    if window_capture.screenshot is None:
        continue

    detector.update(window_capture.screenshot)
    targets = trainers.draw_rectangles(window_capture.screenshot, detector.rectangles)
    click_points = trainers.get_click_points(detector.rectangles)
    print(click_points)
    # if click_points:
    #     for point in click_points:
    #         win32api.SetCursorPos(point)
    #         sleep(1.250)
            

    cv.imshow('Yu-Gi-Oh! DUEL LINKS', window_capture.screenshot)

    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        window_capture.stop()
        detector.stop()
        cv.destroyAllWindows()
        break
    # elif cv.waitKey(1) == ord('p'):
    #     cv.imwrite('positive/{}.jpg'.format(loop_time), window_capture.screenshot)
    # elif cv.waitKey(1) == ord('n'):
    #     cv.imwrite('negative/{}.jpg'.format(loop_time), window_capture.screenshot)

print('Done')