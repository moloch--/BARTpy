'''

BART objects, so we don't have to think about the XML
we just play with Python objects and it's all abstracted away.

'''

import urllib
import urllib2
import platform as py_platform
import xml.etree.cElementTree as ET

from datetime import timedelta


TERM_COLORS = {
    "default": "\033[0m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "blue": "\033[36m",
    # There's actually no ASCI escape for orange :(
    # so I just magenta
    "orange": "\033[35m",
}


class XMLHelper(object):

    ''' Base object with helper functions to deail with XML '''

    def get_first_child(self, et, tag):
        ''' Return a child tag with a given name '''
        kids = filter(lambda child: child.tag == tag, et.getchildren())
        return kids[0] if len(kids) else ValueError("No child tag %s" % tag)

    def get_all_children(self, et, tag):
        return filter(lambda child: child.tag == tag, et.getchildren())


class Train(XMLHelper):

    ''' A single train '''

    def __init__(self, et, departure):
        self.minutes = self.get_first_child(et, 'minutes').text
        self.platform = self.get_first_child(et, 'platform').text
        self.direction = self.get_first_child(et, 'direction').text
        self.length = self.get_first_child(et, 'length').text
        self.color = self.get_first_child(et, 'color').text
        self.hex_color = self.get_first_child(et, 'hexcolor').text
        self.bikes = self.get_first_child(et, 'bikeflag').text
        self.departure = departure

    @property
    def minutes(self):
        ''' Returns the minutes as a timedelta '''
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        ''' Convert annoying "leaving" string to int '''
        if value.lower() == 'leaving':
            value = 0
        self._minutes = timedelta(minutes=int(value))

    @property
    def platform(self):
        return self._platform

    @platform.setter
    def platform(self, value):
        self._platform = int(value)

    @property
    def bikes(self):
        return self._bikes

    @bikes.setter
    def bikes(self, value):
        self._bikes = bool(int(value))

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = int(value)

    @property
    def term_color(self):
        '''
        Return the terminal version of the color, no support for windows
        terminal but for compatability we return an empty string.
        '''
        if py_platform.system().lower() in ['linux', 'darwin']:
            return TERM_COLORS.get(self.color.lower(), "")
        else:
            return ""

    def __str__(self):
        return "%d car %s bound train heading to %s" % (
            len(self), self.direction, self.departure.destination)

    def __len__(self):
        return self._length


class Departure(XMLHelper):

    '''
    This is a basically the train lines/departures to a given destination
    '''

    def __init__(self, et):
        self.destination = self.get_first_child(et, 'destination').text
        self.abbreviation = self.get_first_child(et, 'abbreviation').text
        trains = self.get_all_children(et, 'estimate')
        self.trains = [Train(est, self) for est in trains]

    def __iter__(self):
        for train in self.trains:
            yield train


class Station(XMLHelper):

    ''' The BART stations '''

    def __init__(self, et):
        self.name = self.get_first_child(et, 'name').text
        self.abbreviation = self.get_first_child(et, 'abbr').text
        departures = self.get_all_children(et, 'etd')
        self.departures = [Departure(depart) for depart in departures]

    @property
    def north(self):
        ''' All north bound trains '''
        return filter(lambda train: train.direction.lower() == "north", self)

    @property
    def south(self):
        ''' All south bound trains '''
        return filter(lambda train: train.direction.lower() == "south", self)

    def __getitem__(self, key):
        '''
        We return the Departure for a given key (destination). When we filter
        for the key we get a list, but it will only ever be empty or contain a
        single object, so we return the Departure or None.
        '''
        key = key.lower()
        departs = filter(
            lambda depart: depart.destination.lower() == key, self.departures)
        return departs[0] if len(departs) else None

    def __iter__(self):
        ''' Just iterate all the trains in the station '''
        for departure in self.departures:
            for train in departure:
                yield train


class BART(object):

    '''
    This class represents the entire BART system
    '''

    API_URL = "http://api.bart.gov/api/etd.aspx"

    STATION_NAMES = {
        # Abbr   Station Name
        "12th": "12th St. Oakland City Center",
        "16th": "16th St. Mission",
        "19th": "19th St. Oakland",
        "24th": "24th St. Mission",
        "ashb": "Ashby",
        "balb": "Balboa Park",
        "bayf": "Bay Fair",
        "cast": "Castro Valley",
        "civc": "Civic Center",
        "cols": "Coliseum",
        "colm": "Colma",
        "conc": "Concord",
        "daly": "Daly City",
        "dbrk": "Downtown Berkeley",
        "dubl": ["Dublin", "Pleasanton"],
        "deln": "El Cerrito del Norte",
        "plza": "El Cerrito Plaza",
        "embr": "Embarcadero",
        "frmt": "Fremont",
        "ftvl": "Fruitvale",
        "glen": "Glen Park",
        "hayw": "Hayward",
        "lafy": "Lafayette",
        "lake": "Lake Merritt",
        "mcar": "MacArthur",
        "mlbr": "Millbrae",
        "mont": "Montgomery St.",
        "nbrk": "North Berkeley",
        "ncon": ["North Concord", "Martinez"],
        "orin": "Orinda",
        "pitt": ["Pittsburg", "Bay Point"],
        "phil": "Pleasant Hill",
        "powl": "Powell St.",
        "rich": "Richmond",
        "rock": "Rockridge",
        "sbrn": "San Bruno",
        "sfia": ["SFO", "San Francisco International Airport"],
        "sanl": "San Leandro",
        "shay": "South Hayward",
        "ssan": "South San Francisco",
        "ucty": "Union City",
        "wcrk": "Walnut Creek",
        "wdub": "West Dublin",
        "woak": "West Oakland",
    }

    def __init__(self, api_key='MW9S-E7SL-26DU-VV8V'):
        self.api_key = api_key

    def api_request(self, **parameters):
        '''
        Creates the HTTPRequest object and automatically adds the
        API key.
        '''
        parameters['key'] = self.api_key
        params = urllib.urlencode(parameters)
        response = urllib2.urlopen(self.API_URL + '?' + params)
        return ET.fromstring(response.read())

    def _get_station(self, name):
        '''
        Get the details for a single station from the API.
        TODO: Raise exceptions if the API returns an error.
        '''
        resp = self.api_request(cmd='etd', orig=name)
        kids = resp.getchildren()
        stations = filter(lambda child: child.tag == 'station', kids)
        return Station(stations[0])

    def __getitem__(self, key):
        ''' We handle both the abbreviation and full name '''
        for abbr, name in self.STATION_NAMES.iteritems():
            if key.lower() == abbr or key in name:
                return self._get_station(abbr)
        raise KeyError("Not a valid station name")

    def __iter__(self):
        for station in self.STATION_NAMES:
            yield self[station]
