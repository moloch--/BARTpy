#!/usr/bin/env python
'''
A command line interface to the BART
'''

import argparse
import platform

from BART import BART


if platform.system().lower() in ['linux', 'darwin']:
    INFO = "\033[1m\033[36m[*]\033[0m "
    WARN = "\033[1m\033[31m[!]\033[0m "
    BOLD = "\033[1m"
else:
    INFO = "[*] "
    WARN = "[!] "
    BOLD = ""


def _main(args):
    bart = BART()
    station = bart[args.station]
    for departure in station.departures:
        print "Departures -> %s" % departure.destination
        print "==============" + ("=" * len(departure.destination))
        for index, train in enumerate(departure.estimates):
            print "%d) %d car train in %s" % (
                index + 1, len(train), train.minutes
            )
        print ""


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command line access to BART schedules',
    )
    parser.add_argument('--station', '-s',
                        help='the station to pull information about',
                        dest='station',
                        required=True,)
    _main(parser.parse_args())
