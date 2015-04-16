'''

API Objects

'''

import urllib
import urllib2
import xml.etree.cElementTree as ET

from datetime import timedelta


class XMLParser(object):

    ''' Base object with helper functions to deail with XML '''

    def get_first_child(self, et, tag):
        ''' Return a child tag with a given name '''
        kids = filter(lambda child: child.tag == tag, et.getchildren())
        return kids[0] if len(kids) else ValueError("No child tag %s" % tag)

    def get_all_children(self, et, tag):
        return filter(lambda child: child.tag == tag, et.getchildren())


class Train(XMLParser):

    def __init__(self, et):
        self.minutes = self.get_first_child(et, 'minutes').text
        self.platform = self.get_first_child(et, 'platform').text
        self.direction = self.get_first_child(et, 'direction').text
        self.length = self.get_first_child(et, 'length').text
        self.color = self.get_first_child(et, 'color').text
        self.hex_color = self.get_first_child(et, 'hexcolor').text
        self.bikes = self.get_first_child(et, 'bikeflag').text

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
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

    def __len__(self):
        return self._length


class Departure(XMLParser):

    def __init__(self, et):
        self.destination = self.get_first_child(et, 'destination').text
        self.abbreviation = self.get_first_child(et, 'abbreviation').text
        trains = self.get_all_children(et, 'estimate')
        self._parse_trains(trains)

    def _parse_trains(self, trains):
        self.trains = [Train(est) for est in trains]


class Station(XMLParser):

    def __init__(self, et):
        self.name = self.get_first_child(et, 'name').text
        self.abbreviation = self.get_first_child(et, 'abbr').text
        departures = self.get_all_children(et, 'etd')
        self._parse_departures(departures)

    def _parse_departures(self, departures):
        self.departures = [Departure(depart) for depart in departures]


class BART(object):

    '''
    This class represents the entire BART system
    '''

    API_URL = "http://api.bart.gov/api/etd.aspx"

    STATION_NAMES = {
        # Abbr   Station Name
        "12th": "12th St. Oakland City Center",
        "16th": "16th St. Mission (SF)",
        "19th": "19th St. Oakland",
        "24th": "24th St. Mission (SF)",
        "ashb": "Ashby (Berkeley)",
        "balb": "Balboa Park (SF)",
        "bayf": "Bay Fair (San Leandro)",
        "cast": "Castro Valley",
        "civc": "Civic Center (SF)",
        "cols": "Coliseum/Oakland Airport",
        "colm": "Colma",
        "conc": "Concord",
        "daly": "Daly City",
        "dbrk": "Downtown Berkeley",
        "dubl": "Dublin/Pleasanton",
        "deln": "El Cerrito del Norte",
        "plza": "El Cerrito Plaza",
        "embr": "Embarcadero (SF)",
        "frmt": "Fremont",
        "ftvl": "Fruitvale (Oakland)",
        "glen": "Glen Park (SF)",
        "hayw": "Hayward",
        "lafy": "Lafayette",
        "lake": "Lake Merritt (Oakland)",
        "mcar": "MacArthur (Oakland)",
        "mlbr": "Millbrae",
        "mont": "Montgomery St. (SF)",
        "nbrk": "North Berkeley",
        "ncon": "North Concord/Martinez",
        "orin": "Orinda",
        "pitt": "Pittsburg/Bay Point",
        "phil": "Pleasant Hill",
        "powl": "Powell St. (SF)",
        "rich": "Richmond",
        "rock": "Rockridge (Oakland)",
        "sbrn": "San Bruno",
        "sfia": "San Francisco Int'l Airport",
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

    def __getitem__(self, key):
        ''' We handle both the abbreviation and full name '''
        for abbr, name in self.STATION_NAMES.iteritems():
            if key == abbr or key == name:
                return self._get_station(abbr)
        raise KeyError("Not a valid station name")

    def api_request(self, **parameters):
        '''
        Creates the HTTPRequest object and automatically adds the
        API key and assocaited email
        '''
        parameters['key'] = self.api_key
        params = urllib.urlencode(parameters)
        response = urllib2.urlopen(self.API_URL + '?' + params)
        return ET.fromstring(response.read())

    def _get_station(self, name):
        resp = self.api_request(cmd='etd', orig=name)
        kids = resp.getchildren()
        stations = filter(lambda child: child.tag == 'station', kids)
        return Station(stations[0])
