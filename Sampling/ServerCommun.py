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
SEPARATOR = "$|"
KB = 1024
HALF_KB = 1024/2
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
            raw_signal = conn.recv(HALF_KB)

        except error:
            conn.close()
            return

        finally:
            anona_client_data = parse_anona_client_signal(raw_signal)
            # anona_client[0] is the header from client signal, returned by parsing method
            if anona_client_data[0] == REGISTER_HEADER:
                pass

            if anona_client_data[0] == VALID_SAMPLE_HEADER:
                pass

            if anona_client_data[0] == NEW_SAMPLE_HEADER:
                pass

            if anona_client_data[0] == NEW_SAMPLE_HEADER:
                conn.close()


def parse_anona_client_signal(data):
    """
    :param data: data from socket to client
    :type data: str
    :return: tuple object with header and parsed data
    """
    if data.startswith(REGISTER_HEADER):
        return REGISTER_HEADER, parse_register_signal(data)

    elif data.startswith(VALID_SAMPLE_HEADER):
        return VALID_SAMPLE_HEADER, parse_sample_signal(data)

    elif data.startswith(NEW_SAMPLE_HEADER):
        return NEW_SAMPLE_HEADER, parse_sample_signal(data)

    else:
        return LOG_OUT_HEADER, parse_exit_signal(data)


def parse_register_signal(data):
    """
    :param data: data from socket to client, starts with 'SIGN'
    :type data: srt
    :return: array of user data
    """
    data = data.split(SEPARATOR)[1:]  # Remove header cell
    return data


def parse_sample_signal(data):
    """
    :param data: data from socket to client, starts with 'SMPT'
    :type data: str
    :return: Sample object received from data
    """
    data = data.split(SEPARATOR)[1:]  # Remove header cell
    data[0] = loads(data[0])  # data[0] contains pickled sample
    return data[0]


def parse_exit_signal(data):
    """
    :param data: data from socket to client, starts with 'SMPT'
    :type data: str
    :return: time of log out in str
    """
    return data.split(SEPARATOR)[1]  # data[1] contains time of log out
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
