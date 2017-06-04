import pyrebase
import datetime
import collections

__author__ = 'Gilad Barak'


class DataHandler(object):
    def __init__(self, config, user_name):
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.user = user_name

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

    def stream_data(self):
        pass
