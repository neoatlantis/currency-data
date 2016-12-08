#!/usr/bin/env python

import subprocess
from getCurrencyRates import getCurrencyRates

##############################################################################
# configuration as our interests

conf = {
    "eur_12h": {
        "title": "EUR to CNY Exchange Rates",
        "timespan": (0, -43200),
        "c1s": ['eur'],
        "c2": "cny",
        "xformat": "%H:%M",
    },
    "eur_usd_7d": {
        "title": "EUR/USD to CNY Exchange Rates",
        "timespan": (0, -86400*7),
        "c1s": ['eur'],
        "c2": "cny",
        "xformat": "%m-%d",
    }
}
##############################################################################
# gnuplot ploter


plotdata = ''
plotcmds = []

def newPlot():
    global plotdata, plotcmds
    plotdata = ''
    plotcmds = []

def plot(data, title):
    global plotdata, plotcmds
    datastr = '\n'.join(["%s %s" % (x,y) for x, y in data])
    plotdata += datastr + '\ne\n'
    plotcmds.append('"-" using 1:2 title "%s" with lines' % title)

def endPlot(title, xformat, output):
    global plotdata, plotcmds
    script = """
reset

set term png size 400,300 font "Verdana,9"
set output "%s.png"

set title "%s"

set xdata time
set timefmt "%%s"
set format x "%s"

set xtics rotate 

plot %s
%s
""" % (
        output,
        title,
        xformat,
        ','.join(plotcmds),
        plotdata
    )
    open('.temp.gp', 'w+').write(script)
    subprocess.call(['gnuplot', '.temp.gp'])

##############################################################################
# plot controller

plotcmd = []
for filename in conf:
    newPlot()

    prof = conf[filename]
    t1, t2 = prof['timespan']
    c2 = prof['c2']
    for c1 in prof['c1s']:
        data = getCurrencyRates(c1, c2, t1, t2)
        rkey = ("%s%s" % (c1, c2)).upper()
        
        data = [(i['time'], i[rkey]) for i in data]
        plot(data, rkey)

    endPlot(prof["title"], prof["xformat"], filename)
