import pyrebase
import datetime
import collections

config = {
    "apiKey": "AIzaSyABnZ9KDeJiJxqswHy7rJqVhP5Qu5DOxRo",
    "authDomain": "anona-dd0ad.firebaseapp.com",
    "databaseURL": "https://anona-dd0ad.firebaseio.com",
    "projectId": "anona-dd0ad",
    "storageBucket": "anona-dd0ad.appspot.com",
    "serviceAccount": "/Users/Giladondon/Documents/Cyber/ANONA/AnonaAI/anona-dd0ad-firebase-adminsdk-xzzb7-41f8da447b.json"
  };

firebase = pyrebase.initialize_app(config)
db = firebase.database()
user = db.child("users").child("ayadrori7")
keys = user.child("keys").get()
parsed = {}
for key in keys.each():
    values = key.key().split(" ")
    values[4] = str(int(values[4]) + 1)
    values[6] = 2017
    ts = [ values[6], values[5], values[4], values[0], values[1], values[2], str(int(values[3])*1000) ]
    newdate = datetime.datetime(*map(int, ts))
    parsed[newdate] = key.val()

od = collections.OrderedDict(sorted(parsed.items()))


deltas = []

is_first = True
start = None
count = 0

for item in od:
    count += 1
    if is_first:
        start = item
        is_first = False
    if od[item] == 13:
        deltas.append([(item - start).total_seconds() * 1000, count ])
        is_first = True
        count = 0

print(deltas)

thefile = open('test.txt', 'w')
for item in deltas:
    thefile.write("%s\n" % item)