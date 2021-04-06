from cv2 import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt


class DuelLinksBot:

    # Constantes
    TRAINER_CLICK_WAIT = 5
    END_DUEL_WAIT = 10