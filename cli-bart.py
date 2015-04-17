#!/usr/bin/env python
'''
A command line interface to the BART
'''

import argparse

from BART import BART


def display_trains(station):
    bart = BART()
    for departure in bart[station].departures:
        print "Departures -> %s" % departure.destination
        print "==============" + ("=" * len(departure.destination))
        for index, train in enumerate(departure.trains):
            print "%d) %d car train in %s" % (
                index + 1, len(train), train.minutes
            )
        print ""


def display_station_names():
    print "Abbr - Station Name"
    print "==================="
    for abbr, name in BART.STATION_NAMES.iteritems():
        print "%s - %s" % (abbr, name)


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
