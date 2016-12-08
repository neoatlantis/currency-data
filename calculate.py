#!/usr/bin/env python

import os
import shelve
import sys
import time

BASEPATH = os.path.realpath(os.path.dirname(sys.argv[0]))
filepath = lambda *i: os.path.join(BASEPATH, *i)

try:
    c1, c2, time1, time2 = sys.argv[1:][:4]
    now = time.time()
    c1 = c1.upper().strip()
    c2 = c2.upper().strip()
    assert len(c1) == 3 and len(c2) == 3
    gettime = lambda i: i <= 0 and now + i or i
    time1, time2 = float(time1), float(time2)
    time1 = gettime(time1)
    time2 = gettime(time2)
    timestart = min(time1, time2)
    timeend = max(time1, time2)
except:
    print "Usage: python calculate.py XXX YYY Time1 Time2",
    print "       * XXX, YYY: Name of currency.",
    print "       * Time1, Time2: in seconds. If > 0, it's regarded as a"
    print "         timestamp. Otherwise as offset to the past."
    sys.exit(1)

db = shelve.open(filepath('currencies.db'), flag='c')
data = {}

for key in db:
    timestamp = float(key)
    if timestamp > timeend or timestamp < timestart: continue
    try:
        data[timestamp] = (\
            db[key]['rates'][c1],
            db[key]['rates'][c2]
        )
    except Exception,e:
        print e
        continue

db.close()

output = {}
for t in data:
    entry = {}
    entry['USD%s' % c1] = data[t][0]
    entry['USD%s' % c2] = data[t][1]
    entry['%s%s' % (c1, c2)] = data[t][1] / data[t][0]
    output[t] = entry
print output 
