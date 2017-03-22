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

# -------------- IMPORTS & SETTINGS ----------------
from time import time
import Mouse
from multiprocessing.pool import ThreadPool
# --------------------------------------------------

# --------------- CONSTANTS ------------------------
SAMPLES = {"Mouse Speed": Mouse.mouse_speed_avg_over_time,
           "Mouse Clicks Count": Mouse.count_clicks_over_time,
           "Mouse Distance Covered": Mouse.mouse_distance_over_time}
# --------------------------------------------------

# -------------- FUNCTIONS -------------------------


def manage_threads(time_range, samples_func):
    """
    :param time_range: time range in seconds
    :type time_range: int
    """
    pool = ThreadPool(processes=len(samples_func))

    for key in samples_func.keys():
        samples_func[key] = pool.apply_async(samples_func[key], (time_range, ))

    for key in samples_func.keys():
        samples_func[key] = samples_func[key].get()

    return samples_func


def generate_sample(sampling_dict):
    return Sample(sampling_dict)


def main():
    print manage_threads(10, SAMPLES)

# --------------------------------------------------

# --------------- CLASS ----------------------------


class Sample:
    def __init__(self, sampling_dict):
        """
        :param sampling_dict: dictionary containing all samples made on system on a certain time period
        :type sampling_dict: dict
        """
        self.sampling_dict = sampling_dict
        self.time_stamp = time()

# --------------------------------------------------

# ------------------- MAIN -------------------------

if __name__ == '__main__':
    main()
# --------------------------------------------------
