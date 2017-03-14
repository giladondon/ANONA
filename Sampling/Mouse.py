"""
 ############################################
# Author: Gilad "Giladondon" Barak           #
# Project ANONA - GVAHIM Cyber Program       #
# Last Edited in: __.__.__                   #
# Description:                               #
#                                            #
#                                            #
 ############################################
"""

__author__ = "Gilad Barak"
__name__ = "main"

# --------------- CONSTANTS ------------------------
RIGHT_MOUSE_ID = 0x02
LEFT_MOUSE_ID = 0x01
# --------------------------------------------------

# -------------- IMPORTS & SETTINGS ----------------
from win32api import GetKeyState
from win32gui import GetCursorPos, GetWindowText, GetForegroundWindow, FindWindow
from win32gui import GetScrollInfo
from win32gui import GetActiveWindow
from win32con import SB_HORZ
from time import time
from math import sqrt, pow
# --------------------------------------------------

# -------------- FUNCTIONS -------------------------


def count_clicks_over_time(time_range):
    """
    :param time_range: time_range in seconds
    :type time_range: int
    :return right_clicks, left_clicks: count of clicks
    :type return: tuple of int
    """
    right_clicks = 0
    left_clicks = 0
    state_right = GetKeyState(RIGHT_MOUSE_ID)
    state_left = GetKeyState(LEFT_MOUSE_ID)
    timer_end = time() + time_range
    while time() < timer_end:
        if GetKeyState(LEFT_MOUSE_ID) != state_left:
            if state_left < 0:
                left_clicks += 1
            state_left = GetKeyState(LEFT_MOUSE_ID)
        elif GetKeyState(RIGHT_MOUSE_ID) != state_right:
            if state_right < 0:
                right_clicks += 1
            state_right = GetKeyState(RIGHT_MOUSE_ID)

    return right_clicks, left_clicks


def mouse_distance_over_time(time_range):
    """
    :param time_range: time range in seconds
    :type time_range: int
    :return distance: distance mouse covered over time range
    :type return: double
    """
    timer_end = time() + time_range
    crusor_pos = GetCursorPos()
    distance = 0

    while time() < timer_end:
        if GetCursorPos() != crusor_pos:
            x_delta = (crusor_pos[0] - GetCursorPos()[0])
            y_delta = (crusor_pos[1] - GetCursorPos()[1])
            distance += sqrt(pow(x_delta, 2) + pow(y_delta, 2))
            crusor_pos = GetCursorPos()

    return distance

# --------------------------------------------------

# --------------- CLASS ----------------------------
# --------------------------------------------------

# ------------------- MAIN -------------------------


def main():
    pass

if __name__ == 'main':
    main()
# --------------------------------------------------
