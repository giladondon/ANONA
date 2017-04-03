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
from time import time, gmtime, strftime
import Mouse
from multiprocessing.pool import ThreadPool
import numpy as np
# --------------------------------------------------

# --------------- CONSTANTS ------------------------
SAMPLES = {"Mouse Speed": Mouse.MouseSpeedAverageOverTime(),
           "Mouse Left Clicks Count": Mouse.CountLeftClicksOverTime(),
           "Mouse Right Clicks Count": Mouse.CountRightClicksOverTime(),
           "Mouse Distance Covered": Mouse.MouseDistanceOverTime()}

ROOT_FOR_SAMPLE_FILE = "D:\\sampling-for-anona.txt"
TIME_RANGE_FOR_CLASS = 60*2
TIME_RANGE_FOR_SAMPLE = 10
MOUSE_SPEED = "Mouse Speed"
MOUSE_CLICKS = "Mouse Clicks Count"
MOUSE_DISTANCE = "Mouse Distance Covered"
VALID = True
UNWANTED_CHARS = "'"": "
# --------------------------------------------------

# --------------- CLASS ----------------------------


class Sample:
    def __init__(self, sampling_dict):
        """
        :param sampling_dict: dictionary containing all samples made on system on a certain time period
        :type sampling_dict: dict
        """
        self.sampling_dict = sampling_dict
        self.time_stamp = strftime("%Y %H:%M:%S", gmtime())

    def is_valid(self):
        for aspect in self.sampling_dict.keys():
            if not SAMPLES[aspect].is_valid(self.sampling_dict[aspect]):
                return SAMPLES[aspect].is_valid(self.sampling_dict[aspect])

        return VALID

# --------------------------------------------------


# -------------- FUNCTIONS -------------------------


def manage_threads(time_range, samples_func):
    """
    :param time_range: time range in seconds
    :type time_range: int
    """
    pool = ThreadPool(processes=len(samples_func.keys()))
    samples = {}

    for aspect in samples_func.keys():
        samples[aspect] = pool.apply_async(samples_func[aspect].execute, args=(time_range, ))

    for key in samples_func.keys():
        samples[key] = samples[key].get()

    return samples


def generate_sample(sampling_dict):
    return Sample(sampling_dict)


def make_sets_class(time_range):
    """
    :param time_range: time range in seconds
    :type time_range: int
    """
    timer_ends = time() + time_range
    samples = []

    while time() < timer_ends:
        current_sample = generate_sample(manage_threads(TIME_RANGE_FOR_SAMPLE, SAMPLES))
        if current_sample.is_valid():
            samples.append(current_sample)

    return samples


def parse_samples_numpy(samples_file_handle):
    """
    :param samples_file_handle: file handle for txt sampling file
    :type samples_file_handle: file - txt, open for reading
    """


def main():
    f = open(ROOT_FOR_SAMPLE_FILE, "w")
    dataset = make_sets_class(20)
    for sample in dataset:
        f.write(str(sample.sampling_dict) + "  :  " + str(sample.time_stamp) + "\n")

    f.close()

# --------------------------------------------------

# ------------------- MAIN -------------------------

if __name__ == '__main__':
    main()
# --------------------------------------------------
