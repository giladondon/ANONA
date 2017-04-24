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
IP = "127.0.0.1"
PORT = 555
# --------------------------------------------------

# -------------- IMPORTS & SETTINGS ----------------
from socket import socket
from socket import error
from Sample import *
from pickle import dumps, loads
# --------------------------------------------------

# -------------- FUNCTIONS -------------------------


def connect():
    anona_connection = socket()
    while True:
        try:
            anona_connection.connect((IP, PORT))
            return anona_connection
        except error:
            pass
# --------------------------------------------------

# --------------- CLASS ----------------------------
# --------------------------------------------------

# ------------------- MAIN -------------------------


def main():
    anona_connection = connect()

    while True:
        try:
            anona_connection.send(dumps(desktop_anona_run_sample(TIME_RANGE_FOR_SAMPLE)))
            print anona_connection.recv(1024)
        except error:
            anona_connection = connect()

if __name__ == '__main__':
    main()
# --------------------------------------------------
