import pyrebase
import datetime
import collections
from featuresMaker import FeatureGen
import numpy as np

config = {
    "apiKey": "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo",
    "authDomain": "anona-dd0ad.firebaseapp.com",
    "databaseURL": "https://anona-dd0ad.firebaseio.com",
    "projectId": "anona-dd0ad",
    "storageBucket": "anona-dd0ad.appspot.com",
    "serviceAccount": "/Users/Giladondon/Documents/Cyber/ANONA/AnonaAI/anona-dd0ad-firebase-adminsdk-xzzb7-41f8da447b.json"
  };

#may13laniado
#giladondon
firebase = pyrebase.initialize_app(config)
db = firebase.database()
user = db.child("users").child("giladondon")
keys = user.child("keys").get()
parsed = {}
for key in keys.each():
    values = key.key().split(" ")
    if (values[6] == 117):
        values[6] = 2017
    values[4] = str(int(values[4]) + 1)
    ts = [ values[6], values[5], values[4], values[0], values[1], values[2], str(int(values[3])*1000) ]
    newdate = datetime.datetime(*map(int, ts))
    parsed[newdate] = key.val()

od = collections.OrderedDict(sorted(parsed.items()))


def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

my_stream = db.child("users").child("giladondon").child("keys").stream(stream_handler)

print "A"




results = FeatureGen.punctuation_marks(od.values())
results = np.array(results)

print results

results = FeatureGen.backspace_count(od.values())
results = np.array(results)

print results

results = FeatureGen.type_rate(od)
results = np.array(results)

print results

# thefile = open('test.txt', 'w')
#
# with open('test.txt', 'w') as fp:
#     fp.write('\n'.join('%s,%s' % x for x in results))







# deltas = []
#
# is_first = True
# start = None
# count = 0
#
# for item in od:
#     count += 1
#     if is_first:
#         start = item
#         is_first = False
#     if od[item] == 13:
#         deltas.append([ (item - start).total_seconds() * 1000, count ])
#         is_first = True
#         count = 0
#
# print(deltas)


# for item in deltas:
#   thefile.write("%s\n" % item)



