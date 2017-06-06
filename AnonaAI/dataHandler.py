import pyrebase
import datetime
import collections
from DeepLearning import NeuralNetwork
from featuresMaker import FeatureGen
import numpy as np

__author__ = 'Gilad Barak'
__name__ = "main"

USER_NAME = "giladondon"
JSON_PATH = "/Users/Giladondon/Documents/Cyber/ANONA/AnonaAI/model.json"
WEIGHTS_PATH = "/Users/Giladondon/Documents/Cyber/ANONA/AnonaAI/model.h5"
ENTER_CODE = 13
YEAR_CELL_INDEX = 6
KEYS_TREE_ACCESS = "keys"
USER_TREE_ACCESS = "users"


class DataHandler(object):
    """
    DataHandler deals with firebase-database communication
    """

    def __init__(self, config, user_name):
        """
        :param config: configuration dictionary as required to access database as ADMIN
        :param user_name: name of user to work on, each dataHandler works with one client
        """
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.user = user_name
        self.new_samples = {}
        self.data_stream = None

    @staticmethod
    def generate_date(values):
        """
        :param values: parsed date by spaces as saved in database
        :return: date in correct format as needed for deep learning
        """
        values[4] = str(int(values[4]) + 1)
        ts = [values[6], values[5], values[4], values[0], values[1], values[2], str(int(values[3]) * 1000)]
        new_date = datetime.datetime(*map(int, ts))

        return new_date

    @staticmethod
    def is_fixed(values):
        """
        :param values: parsed date by spaces as saved in database
        :return: True if date is correctly represented
        """
        return values[YEAR_CELL_INDEX] == 2017

    def fix_date(self, values):
        """
        As I started working on the database from client side I was using a wrong date representation
        which I only changed after a long time. Meanwhile I was collecting data from users - data I wasn't
        going to lose. this function takes care of my F*ck up
        :param values: parsed date by spaces as saved in database
        :return: correct date
        """
        values[YEAR_CELL_INDEX] = 2017

        return self.generate_date(values)

    def get_data(self):
        user_db = self.db.child(USER_TREE_ACCESS).child(self.user)
        keys = user_db.child(KEYS_TREE_ACCESS).get()

        parsed = {}

        for key in keys.each():
            values = key.key().split(" ")
            if not self.is_fixed(values):
                self.fix_date(values)
            parsed[self.generate_date(values)] = key.val()

        return collections.OrderedDict(sorted(parsed.items()))

    def stream_data(self, stream_hand):
        print "user/" + str(self.user) + "/keys"
        self.data_stream = self.db.child(USER_TREE_ACCESS).child(str(self.user)).child(KEYS_TREE_ACCESS).stream(
            stream_hand)


global samples_queue, anona, config
samples_queue = {}
config = {
    "apiKey": "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo",
    "authDomain": "anona-dd0ad.firebaseapp.com",
    "databaseURL": "https://anona-dd0ad.firebaseio.com",
    "projectId": "anona-dd0ad",
    "storageBucket": "anona-dd0ad.appspot.com",
    "serviceAccount": "/Users/Giladondon/Documents/Cyber/ANONA/AnonaAI/anona-dd0ad-firebase-adminsdk-xzzb7-41f8da447b.json"
}
anona = DataHandler(config, USER_NAME)
is_first = True


def run_prediction():
    od_sample_queue = collections.OrderedDict(sorted(samples_queue.items()))

    punctuation_samples = np.array(FeatureGen.punctuation_marks(od_sample_queue.values()))

    backspace_samples = np.array(FeatureGen.backspace_count(od_sample_queue.values()))

    type_pace_samples = np.array(FeatureGen.type_rate(od_sample_queue))

    new_data = prepare_data(punctuation_samples, type_pace_samples, backspace_samples)

    nn = NeuralNetwork()

    model = nn.load_model(JSON_PATH, WEIGHTS_PATH)

    print model.predict_proba(new_data)


def stream_handler(message):
    global is_first
    if not is_first:
        for key, value in message["data"].iteritems():
            key = key.split(" ")
            if not anona.is_fixed(key):
                key = anona.fix_date(key)
            else:
                key = anona.generate_date(key)

            samples_queue[key] = value
            print str(key) + "-" + str(samples_queue[key])

            if value == ENTER_CODE:
                try:
                    run_prediction()
                finally:
                    samples_queue.clear()
    else:
        is_first = False


def prepare_data(punc, speed, backspace):
    samples = punc
    samples = np.concatenate((samples, speed), axis=1)
    samples = np.concatenate((samples, backspace), axis=1)

    return samples


def main():
    anona.stream_data(stream_handler)
    """
    stream_handler({"data": {u'6 5 35 524 6 6 2017': 8}, "event": "patch", "path": "/"})
    stream_handler({"data": {u'6 5 35 682 6 6 2017': 8}, "event": "patch", "path": "/"})
    stream_handler({"data": {u'6 5 36 497 6 6 2017': 1499}, "event": "patch", "path": "/"})
    stream_handler({"data": {u'6 5 37 9 6 6 2017': 1497}, "event": "patch", "path": "/"})
    stream_handler({"data": {u'6 5 37 167 6 6 2017': 1496}, "event": "patch", "path": "/"})
    stream_handler({"data": {u'6 5 37 950 6 6 2017': 16}, "event": "patch", "path": "/"})
    stream_handler({"data": {u'6 5 38 192 6 6 2017': 13}, "event": "patch", "path": "/"})
    """

if __name__ == "main":
    main()
