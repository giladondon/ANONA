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

# --------------- CONSTANTS ------------------------
# --------------------------------------------------

# -------------- IMPORTS & SETTINGS ----------------
from time import time
# --------------------------------------------------

# -------------- FUNCTIONS -------------------------
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


def main():
    pass


if __name__ == '__main__':
    main()
# --------------------------------------------------
