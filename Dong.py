import sys
import math
import cv2
import time
import numpy as np
from djitellopy import Tello


YOLO_DIR = 'yolov5'
MODEL_DIR = 'models/best5n2.pt'

RADIUS = 0
HEIGHT = 150
DIST = 400
YFOV = 49
HFOV = 65
PATH = 's' 

def main():
    aop = 0
    x = 0
    y = 0
    z = 0

    allo = Tello()
    allo.connect()
    allo.streamon()
    frame_read = allo.get_frame_read()
    allo.takeoff()
    time.sleep(1)
    allo.move_up(HEIGHT-allo.get_distance_tof())

    trashy = trash_finder(YOLO_DIR,MODEL_DIR)
    if PATH == 'c':
        path = cpath_setter(HFOV,HEIGHT,RADIUS)

        for position in path:
            allo.send_command_without_return("command")
            x_travel = position[0]-x
            z_travel = position[1]-z
            if x_travel != 0:
                if x_travel > 0:
                    allo.move_forward(abs(x_travel))
                    time.sleep(1)
                elif x_travel < 0:
                    allo.move_back(abs(x_travel))
                    time.sleep(1)
                x += abs(x_travel)
            elif z_travel != 0:
                if z_travel > 0:
                    z_travel = abs(z_travel)  // 10
                    for i in range(10):
                        allo.send_command_without_return("command")
                        img = frame_read.frame
                        cv2.imshow('yolo',img)
                        ##results = trashy.find_trash(img)
                    ## aop += len(results)
                    ## cv2.imshow('YOLO', np.squeeze(results.render()))
                        allo.move_left(z_travel)
                        time.sleep(1)

                elif z_travel < 0:
                    z_travel = abs(z_travel) // 10
                    for i in range(10):
                        allo.send_command_without_return("command")
                        img = frame_read.frame
                        cv2.imshow('yolo',img)
                        ##results = trashy.find_trash(img)
                    ## aop += len(results)
                    ## cv2.imshow('YOLO', np.squeeze(results.render()))
                        allo.move_right(z_travel)
                        time.sleep(1)

    elif PATH == 's':
        allo.send_command_without_return("command")
        path = spath_setter(YFOV,HEIGHT,0,DIST)
        allo.send_command_without_return("command")
        x = 0
        y = HEIGHT
        z = 0
        for p in path:
            d = p[0]-x
            allo.move_forward(d)
            time.sleep(3)
            allo.send_command_without_return("command")
            img = frame_read.frame
            results = trashy.find_trash(img)
            aop += len(results.pandas().xyxy[0])
            crops = results.crop(save=True)
           # cv2.imshow('YOLO', np.squeeze(results.render()))
            x+= d
    
    allo.streamoff()
    allo.land()
    print("Number Of Pollutants Detected: " + str(aop))


if __name__ == "__main__":
   main()

