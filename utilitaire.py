from typing import Tuple
import time
from graphics import *

FPS = 60
DPF = 1/FPS

def millis_to_second(millis) -> float:
    return millis*(10**-3)

def second_to_millis(second) -> int:
    return int(second*(10**3))

def addition_tuple(tuple1, tuple2) -> Tuple[float, float]:
    return int(tuple1[0] + tuple2[0]), int(tuple1[1] + tuple2[1])

def soustraction_tuple(tuple1, tuple2) -> Tuple[float, float]:
    return int(tuple1[0] - tuple2[0]), int(tuple1[1] - tuple2[1])

def multiplication_tuple(tuple, x : float):
    return tuple.__class__([i*x for i in tuple])

def clamp(val, min_val, max_val):
    return min(max(val, min_val), max_val)

def sign(x : int) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def moyenne_array(array):
    return sum(array)/len(array)

def min_array(array):
    mini = array[0]
    for i in range(1,len(array)):
        mini = min(mini, array[i])
    return mini

TIME_UNTIL_FPS_AVERAGE = 1.0
def frame_handling(interface):
    """
    Met à jour les variables necessaires pour faire tourner le jeu en respectant le nombre d'images par secondes.
    """
    # TUFA = Time Until Frame Average | wait until metrics
    if interface.act_time - interface.TUFA_last_refresh > TIME_UNTIL_FPS_AVERAGE:
        interface.displayed_frame_array = interface.frame_array.copy()
        interface.TUFA_last_refresh = interface.act_time
        interface.frame_array.clear()
    interface.time_to_wait = max(DPF - (time.time() - interface.last_chronos_time), 0)
    time.sleep(interface.time_to_wait)
    interface.act_time = time.time()
    interface.frames += 1
    interface.delta_time = time.time() - interface.last_chronos_time
    interface.last_chronos_time = time.time()
    if len(interface.frame_array) >= FPS:
        interface.frame_array.pop(0)
    interface.frame_array.append(1 / interface.delta_time)

    affiche_tout()