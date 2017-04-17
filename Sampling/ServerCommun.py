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
IP = "0.0.0.0"
PORT = 555
MAXIMUM_LISTEN = 1
REGISTER_HEADER = "SIGN"
VALID_SAMPLE_HEADER = "SMPT"
NEW_SAMPLE_HEADER = "SMPN"
LOG_OUT_HEADER = "EXIT"
# --------------------------------------------------

# -------------- IMPORTS & SETTINGS ----------------
from socket import socket, error
from thread import start_new_thread
from Sample import *
from pickle import dumps, loads
# --------------------------------------------------

# -------------- FUNCTIONS -------------------------


def client_approach(conn):
    """
    :param conn: socket to anona client, for thread use
    :type conn: _socketobject
    """
    while True:
        try:
            loads(conn.recv(1024)).print_sample()
            conn.send("OK")
        except error:
            return


def parse_anona_client_signal(data):
    """
    :param data: data from socket to client
    :type data: str
    """

# --------------------------------------------------

# --------------- CLASS ----------------------------
# --------------------------------------------------

# ------------------- MAIN -------------------------


def main():
    anona_connect = socket()
    anona_connect.bind((IP, PORT))

    while True:
        anona_connect.listen(MAXIMUM_LISTEN)
        client_conn, client_address = anona_connect.accept()
        start_new_thread(client_approach, (client_conn,))

    anona_connect.close()

if __name__ == '__main__':
    main()
# --------------------------------------------------
