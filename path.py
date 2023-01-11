import math
import time
import matplotlib.pyplot as plt

def cpath_setter(hfov,height,radius):
    total_distance = 0
    x = 0
    y = 0
    y_previous = 0
    path = []
    dist_between = math.ceil(2*(height)*math.tan(math.radians(hfov/2)))
    iters = math.ceil((2*radius)/dist_between)

    for z in range(iters):
        path.append((x,y))
        x+=dist_between
        total_distance+=dist_between
        path.append((x,y))
        if x < 2*radius:
            if x % (2*dist_between) != 0:
                y=int(math.sqrt((radius**2)-((x-radius)**2)))
            else:
                y=-int(math.sqrt((radius**2)-((x-radius)**2)))
            total_distance+=math.dist((x,y_previous),(x,y))
            y_previous = y
        else:
            y = 0
    return path

def spath_setter(yfov,height,x1,x2):
    total_distance = abs(x2-x1)
    x = 0
    path = []
    dist_between = math.ceil(2*(height)*math.tan(math.radians(yfov/2)))
    iters = math.ceil(total_distance/dist_between)
    for i in range(iters):
        path.append((x,0))
        x += dist_between
    if (x2,0) not in path:
        path.append((x2,0))
    return path

