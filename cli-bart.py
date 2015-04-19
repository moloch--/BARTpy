#!/usr/bin/env python
'''
A command line interface to the BART
'''

import argparse
import platform

from BART import BART

BOLD = ""
DEFAULT = ""

# Pretty colors for the good operating systems
if platform.system().lower() in ['linux', 'darwin']:
    BOLD = "\033[1m"
    DEFAULT = "\033[0m"


def display_trains(station):
    bart = BART()
    for departure in bart[station].departures:
        print("%sDepartures -> %s%s" % (
            BOLD, departure.destination, DEFAULT,
        ))
        print("==============" + ("=" * len(departure.destination)))
        for index, train in enumerate(departure.trains):
            print("%s%d) %d car train in %s%s" % (
                BOLD + train.term_color, index + 1, len(train),
                train.minutes, DEFAULT,
            ))
        print("")


def display_station_names():
    print("Abbr - Station Name")
    print("===================")
    for abbr, name in BART.STATION_NAMES.iteritems():
        print("%s - %s" % (abbr, name))


def _main(args):
    if args.ls:
        display_station_names()
    if args.station is not None:
        display_trains(args.station)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Command line access to BART schedules',
    )
    parser.add_argument('--station', '-s',
                        help='the station to pull information about',
                        dest='station')
    parser.add_argument('--list', '-l',
                        help='list all station names',
                        action='store_true',
                        dest='ls')
    _main(parser.parse_args())
