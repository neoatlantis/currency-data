#!/usr/bin/env python

import os
import time
import requests
import shelve
import sys

BASEPATH = os.path.realpath(os.path.dirname(sys.argv[0]))
filepath = lambda *i: os.path.join(BASEPATH, *i)

# check for api key
try:
    apikeyFilepath = filepath('apikey')
    apikey = open(apikeyFilepath).read().strip()
except:
    print "Put your API key at `openexchangerates.org` into file `apikey`."
    sys.exit(1)

# check for database
db = shelve.open(filepath('currencies.db'), flag='c')
latest = 0
for key in db:
    timestamp = float(key)
    if timestamp > latest:
        latest = timestamp
if time.time() - latest < 3600 and 'force' not in sys.argv:
    print "You are requesting too frequent. Abandoned to prevent API",
    print "exhaustion. Use `force` in command line to force a request."
    db.close()
    sys.exit(2)

# fetch url
url = "https://openexchangerates.org/api/latest.json?app_id=%s" % apikey

try:
    req = requests.get(url)
    if req.status_code != 200: raise
    json = req.json()
except:
    print "Failed fetching newest data. Abort."
    sys.exit(3)

delkeys = [u'license', u'disclaimer']
for each in delkeys:
    if json.has_key(each): del json[each]

db[str(time.time())] = json
db.close()
sys.exit(0)
