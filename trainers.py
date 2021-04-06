from cv2 import cv2 as cv
import numpy as np

class Trainers:

    # Busca los rectangulos en los que podemos clickar
    def get_click_points(self, rectangles):
        points = []

        # Loop por todos los rectangulos
        for (x, y, w, h) in rectangles:
            # Determinar el centro
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Guardar los puntos
            points.append((center_x, center_y))

        return points

    # Pinta los rectangulos en los entrenadores que corresponda
    def draw_rectangles(self, background_img, rectangles):
        # Color RGB (Verde)
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # Determinar la posicion de la caja
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # Pintamos la caja
            cv.rectangle(background_img, top_left, bottom_right, line_color, lineType=line_type)

        return background_img

    # Pintamos la cruz en el centro
    def draw_crosshairs(self, background_img, points):
        # Color RGB (Rosa)
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            # Pintamos el centro
            cv.drawMarker(background_img, (center_x, center_y), marker_color, marker_type)

        return background_img

    def centeroid(self, point_list):
        point_list = np.asarray(point_list, dtype=np.int32)
        length = point_list.shape[0]
        sum_x = np.sum(point_list[:, 0])
        sum_y = np.sum(point_list[:, 1])
        return [np.floor_divide(sum_x, length), np.floor_divide(sum_y, length)]