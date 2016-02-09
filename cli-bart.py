#!/usr/bin/env python
'''
A command line interface to the BART
'''

import sys
import argparse
import platform

from BART import BART

BOLD = ""
DEFAULT = ""

# Pretty colors for the good operating systems
if platform.system().lower() in ['linux', 'darwin']:
    BOLD = "\033[1m"
    DEFAULT = "\033[0m"


def display_trains(station, no_color=False):
    bart = BART()
    for departure in bart[station].departures:
        if not no_color:
            sys.stdout.write(BOLD)
        sys.stdout.write("Departures -> %s" % (departure.destination))
        if not no_color:
            sys.stdout.write(DEFAULT)
        print("\n==============" + ("=" * len(departure.destination)))
        for index, train in enumerate(departure.trains):
            if not no_color:
                sys.stdout.write(BOLD + train.term_color)
            sys.stdout.write("%d) %d car train in %s" % (
                index + 1, len(train), train.minutes,
            ))
            if not no_color:
                sys.stdout.write(DEFAULT)
            sys.stdout.write("\n")
        sys.stdout.write("---\n")


def display_station_names():
    print("Abbr - Station Name")
    print("===================")
    for abbr, name in BART.STATION_NAMES.iteritems():
        print("%s - %s" % (abbr, name))


def _main(args):
    if args.ls:
        display_station_names()
    if args.station is not None:
        display_trains(args.station, args.no_color)


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
    parser.add_argument('--no-color', '-c',
                        help='disable terminal colors',
                        action='store_true',
                        dest='no_color')
    _main(parser.parse_args())
