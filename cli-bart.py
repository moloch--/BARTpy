#!/usr/bin/env python
'''
A command line interface to the BART
'''

import argparse

from BART import BART


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
