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
user = db.child("users").child("giladondon")
keys = user.child("keys").get()
parsed = {}
for key in keys.each():
    values = key.key().split(" ")
    if len(values[6]) != 4:
        values[4] = str(int(values[4]) + 1)
        values[6] = 2017
        ts = [values[6], values[5], values[4], values[0], values[1], values[2], str(int(values[3])*1000)]
        newdate = datetime.datetime(*map(int, ts))
        parsed[newdate] = key.val()
    elif len(values[6]) == 4:
        ts = [values[6], values[5], values[4], values[0], values[1], values[2], str(int(values[3])*1000)]
        newdate = datetime.datetime(*map(int, ts))
        parsed[newdate] = key.val()

od = collections.OrderedDict(sorted(parsed.items()))


def stream_handler(message):
    print "A"
    print message

my_stream = db.child("users/giladondon").stream(stream_handler, None)


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

backspace_ratio = []

key_count = 0
backspace_count = 0

for item in od:
    key_count += 1
    if od[item] == 13:
        backspace_ratio.append([backspace_count, key_count])
        key_count = 0
        backspace_count = 0
    elif od[item] == 8:
        backspace_count += 1

print(backspace_ratio)

language_shift_ratio = []

key_count = 0
language_shift_count = 0
suspect_shift = False, 0

for item in od:
    key_count += 1

    if od[item] == 18 or od[item] == 16:
        if suspect_shift[0]:
            if suspect_shift[1] != od[item]:
                language_shift_count += 1
                suspect_shift = False, 0
        else:
            suspect_shift = True, od[item]

    if od[item] == 13:
        language_shift_ratio.append([language_shift_count, key_count])
        key_count = 0
        language_shift_count = 0

print language_shift_ratio

punctuation_ratio = []

punctuation_count = 0
key_count = 0

PUNCTUATION_CODES = range(33, 48) + range(58, 65) + range(91, 97) + range(123, 154)

for item in od:
    key_count += 1

    if od[item] in PUNCTUATION_CODES:
        punctuation_count += 1

    if od[item] == 13:
        punctuation_ratio.append([punctuation_count, key_count])
        key_count = 0
        punctuation_count = 0

print punctuation_ratio

print len(backspace_ratio)
print len(deltas)
print len(language_shift_ratio)
print len(punctuation_ratio)

thefile = open('test.txt', 'w')
for item in deltas:
    thefile.write("%s\n" % item)