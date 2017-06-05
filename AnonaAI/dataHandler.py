import pyrebase
import datetime
import collections

__author__ = 'Gilad Barak'
__name__ = "main"


class DataHandler(object):
    def __init__(self, config, user_name):
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.user = user_name
        self.new_samples = {}
        self.data_stream = None

    @staticmethod
    def generate_date(values):
        ts = [values[6], values[5], values[4], values[0], values[1], values[2], str(int(values[3])*1000)]
        new_date = datetime.datetime(*map(int, ts))

        return new_date

    @staticmethod
    def is_fixed(values):
        return len(values[6]) != 4

    def fix_date(self, values):
        values[4] = str(int(values[4]) + 1)
        values[6] = 2017

        return self.generate_date(values)

    def get_data(self):
        user_db = self.db.child("users").child(self.user)
        keys = user_db.child("keys").get()

        parsed = {}

        for key in keys.each():
            values = key.key().split(" ")

            if not self.is_fixed(values):
                parsed[self.fix_date(values)] = key.val()

            elif self.is_fixed(values):
                parsed[self.generate_date(values)] = key.val()

        return collections.OrderedDict(sorted(parsed.items()))

    def stream_handler(self, message):
        try:
            self.new_samples[message["data"].key()] = message["data"].val()
        except AttributeError:
            pass
        finally:
            print message["data"]

    def stream_data(self):
        self.data_stream = self.db.child(self.user + "/keys").stream(self.stream_handler)


if __name__ == "main":
    config = {
    "apiKey": "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo",
    "authDomain": "anona-dd0ad.firebaseapp.com",
    "databaseURL": "https://anona-dd0ad.firebaseio.com",
    "projectId": "anona-dd0ad",
    "storageBucket": "anona-dd0ad.appspot.com",
    "serviceAccount": "/Users/Giladondon/Documents/Cyber/ANONA/AnonaAI/anona-dd0ad-firebase-adminsdk-xzzb7-41f8da447b.json"
    }

    anona = DataHandler(config, "giladondon")
    anona.stream_data()
