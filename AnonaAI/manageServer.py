"""
Basically we need to think of 2 things right now:
- users that are already in the database needs special caring
I need to go through what I already have on them and learn from it
after that I can start service them with my shit.
- users who just signed up while server is up
So that's a piece of cake compared to the other scenario.
If they have nothing on the database I'm gonna get a stream of their shit and instantly give them
my services.

Also think about counting my samples and seeing when I can start service based on that. K?
"""


__name__ = "main"
__author__ = "Gilad Barak"

API_KEY = "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo"
AUTH_DOMAIN = "anona-dd0ad.firebaseapp.com"
DATABASE_URL = "https://anona-dd0ad.firebaseio.com"
STORAGE_BUCKET = "anona-dd0ad.appspot.com"
SERVICE_ACCOUNT = "C:\Heights\Documents\Projects\\anonaAiProj\AnonaAI\\anona-dd0ad-firebase-adminsdk-xzzb7-41f8da447b.json"


import pyrebase
import thread


def set_up_firebase():
    config = {
        "apiKey": API_KEY,
        "authDomain": AUTH_DOMAIN,
        "databaseURL": DATABASE_URL,
        "storageBucket": STORAGE_BUCKET,
        "serviceAccount": SERVICE_ACCOUNT
    }

    return pyrebase.initialize_app(config)


def get_users_firebase(database):
    """
    :param database: firebase database reference
    :return users: array of users child database name
    """
    users = []

    all_users = database.child("users").get()

    for user in all_users.each():
        users.append(user.key())

    return users


def main():
    firebase = set_up_firebase()
    database = firebase.database()

    users = get_users_firebase(database)

    for user in users:
        thread.start_new_thread()  # New thread for every client

    # add Listener for new signing in users



if __name__ == "main":
    main()