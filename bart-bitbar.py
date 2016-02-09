#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <bitbar.title>BART</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Moloch</bitbar.author>
# <bitbar.author.github>moloch--</bitbar.author.github>
# <bitbar.desc>Get BART times.</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

STATION="24th"

# Code
from BART import BART
bart = BART()

print "BART | dropdown=false"
print "%s" % BART.STATION_NAMES[STATION]

for departure in bart[STATION].departures:
    print "---"
    print "%s| color=white" % (departure.destination)
    for index, train in enumerate(departure.trains):
        print "%d) %d car train in %s | color=%s" % (
            index + 1, len(train), train.minutes, train.color)
