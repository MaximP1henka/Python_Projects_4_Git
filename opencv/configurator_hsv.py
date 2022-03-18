import pyautogui as pag
import numpy as np
import cv2
from mss import mss
import sys


class Configurator():

    def __init__(self, window_size: dict = None, ):
        if window_size is None:
            self.window_size = (0, 0, 200, 200)
        else:
            self.window_size = window_size
        self.sct = mss()

    def main_loop(self):

        self.window_settings()

        while True:

            img = np.asarray(self.sct.grab(self.window_size))
            self.window_before_changes(img=img)
            self.window_result(img=img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            if cv2.waitKey(26) & 0xFF == ord("w"):
                print(self.hsv_result)


    def window_settings(self):
        cv2.namedWindow("settings")
        cv2.createTrackbar('h1', 'settings', 0, 255, self.__nothing)
        cv2.createTrackbar('s1', 'settings', 0, 255, self.__nothing)
        cv2.createTrackbar('v1', 'settings', 0, 255, self.__nothing)
        cv2.createTrackbar('h2', 'settings', 255, 255, self.__nothing)
        cv2.createTrackbar('s2', 'settings', 255, 255, self.__nothing)
        cv2.createTrackbar('v2', 'settings', 255, 255, self.__nothing)
        self.crange = [0, 0, 0, 0, 0, 0]

    def window_before_changes(self, img):
        cv2.namedWindow("before_changes")
        cv2.imshow("before_changes", img)

    def window_result(self, img):
        cv2.namedWindow("result")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')
        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        self.hsv_result = (h1,s1,v1,h2,s2,v2)

        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        cv2.imshow("result", thresh)

    @staticmethod
    def __nothing(*args):
        pass


if __name__ == '__main__':
    argv = sys.argv[1:]
    # print(argv)
    config = Configurator()
    config.main_loop()
