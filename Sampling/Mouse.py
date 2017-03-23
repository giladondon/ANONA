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


class CountClicksOverTime:

    def __init__(self):
        self.result = 0

    def execute(self, time_range):
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

        self.result = right_clicks, left_clicks
        return self.result

    @staticmethod
    def is_valid(result):
        return True


class MouseDistanceOverTime:

    def __init__(self):
        self.result = 0

    def execute(self, time_range):
        """
        :param time_range: time range in seconds
        :type time_range: int
        :return distance: distance mouse covered over time range
        :type return: double
        """
        timer_end = time() + time_range
        cursor = GetCursorPos()
        distance = 0

        while time() < timer_end:
            if GetCursorPos() != cursor:
                x_delta = (cursor[0] - GetCursorPos()[0])
                y_delta = (cursor[1] - GetCursorPos()[1])
                distance += sqrt(pow(x_delta, 2) + pow(y_delta, 2))
                cursor = GetCursorPos()

        self.result = distance
        return self.result

    @staticmethod
    def is_valid(result):
        return result > 0


class MouseSpeedAverageOverTime:

    def __init__(self):
        self.result = 0

    def execute(self, time_range):
        """
        :param time_range: time range in seconds
        :type time_range: int
        :return speeds average: averages of mouse speeds over time
        """
        movements_count = 0
        speeds_sum = 0
        movement_timer = time()

        timer_ends = time() + time_range
        cursor_pos = GetCursorPos()
        while time() < timer_ends:
            if cursor_pos != GetCursorPos():
                movement_timer = time()
            if cursor_pos == GetCursorPos():
                speeds_sum += time() - movement_timer
                movements_count += 1

        self.result = speeds_sum / movements_count
        return self.result

    @staticmethod
    def is_valid(result):
        return result > 0

# --------------------------------------------------

# --------------- CLASS ----------------------------
# --------------------------------------------------

# ------------------- MAIN -------------------------


def main():
    pass

if __name__ == 'main':
    main()
# --------------------------------------------------
