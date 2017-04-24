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

ROOT_FOR_SAMPLE_FILE = "C:\\Coding\\sampling-for-anona.txt"
TIME_RANGE_FOR_CLASS = 60*2
TIME_RANGE_FOR_SAMPLE = 5
MOUSE_SPEED = "Mouse Speed"
MOUSE_CLICKS = "Mouse Clicks Count"
MOUSE_DISTANCE = "Mouse Distance Covered"
VALID = True
UNWANTED_CHARS = ("'", " ", "{", "\\n", '"')
REGEX_DATE_START = 3
REGEX_DATE_ENDS = 16
SAMPLE_FEATURE_TEXT = "{}: {}"
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

    def refactor_time_stamp(self, time_stamp):
        self.time_stamp = time_stamp

    def is_valid(self):
        for aspect in self.sampling_dict.keys():
            if not SAMPLES[aspect].is_valid(self.sampling_dict[aspect]):
                return SAMPLES[aspect].is_valid(self.sampling_dict[aspect])

        return VALID

    def print_sample(self):
        for key in self.sampling_dict.keys():
            print SAMPLE_FEATURE_TEXT.format(key, self.sampling_dict[key])
        print str(self.time_stamp)
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

    pool.close()
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


def desktop_anona_run_sample(sample_time_length):
    """
    :param sample_time_length: one sample cover a certain time period (given in seconds
    :type sample_time_length: int
    """
    return generate_sample(manage_threads(sample_time_length, SAMPLES))


def parse_samples_text_file(samples_list):
    """
    :param samples_list: list of text samples
    :type samples_list: list of strings, each cell is sample line over time range
    """
    for i in xrange(len(samples_list)):
        samples_list[i] = samples_list[i].split("}")
        samples_list[i][0] = refactor_sample(samples_list[i][0])
        samples_list[i][1] = samples_list[i][1][REGEX_DATE_START:REGEX_DATE_ENDS]

    return samples_list


def refactor_sample(text_sample):
    """
    :param text_sample: sample side from text file made for class use
    :type text_sample: str
    """
    for char in UNWANTED_CHARS:
        text_sample = text_sample.replace(char, "")

    text_sample = text_sample.split(",")

    sample_dict = {}

    for i in xrange(len(text_sample)):
        text_sample[i] = text_sample[i].split(":")
        text_sample[i][1] = float(text_sample[i][1])
        sample_dict[text_sample[i][0]] = text_sample[i][1]

    return sample_dict


def make_sample_file_class_use(time_range):
    """
    :param time_range: time range in seconds
    :type time_range: int
    """
    f = open(ROOT_FOR_SAMPLE_FILE, "w")
    dataset = make_sets_class(time_range)
    for sample in dataset:
        f.write(str(sample.sampling_dict) + " : " + str(sample.time_stamp) + "\n")

    f.close()
# --------------------------------------------------

# ------------------- MAIN -------------------------


def main():

    make_sample_file_class_use(time_range=20)

    f = open(ROOT_FOR_SAMPLE_FILE, "r")
    dataset = f.readlines()

    print parse_samples_text_file(dataset)

if __name__ == '__main__':
    main()
# --------------------------------------------------
