# scrape a website

# check details
#    address
#   price
#   rooms
#   distance to nearest trainstation

# if match
#    get pictures
#    summarise

import googlemaps
import secrets
import urllib.parse
import requests

gmaps = googlemaps.Client(key=secrets.matrix_api_key)

suburb_list = []


#####################
# Search class
#####################

class HouseType():
    """docstring for ClassName"""
    def __init__(self, locations=[], property_type=[], min_beds=None,
                 max_beds=None, min_price=None, max_price=None, bathrooms=None,
                 car_spaces=None):

        self.locations = locations
        self.property_type = []
        self.min_beds = min_beds
        self.max_beds = max_beds
        self.min_price = min_price
        self.max_price = max_price
        self.bathrooms = bathrooms
        self.car_spaces = car_spaces
        self.listing_results = []  # a list of objects that are successfull matches


    def realestate_url(self):
        """Creates a url to use with realestate.com.au searches"""
        url = "https://www.realestate.com.au/rent/property-townhouse-unit+apartment-house-between-0-1100-in-"
        for i, item in enumerate(self.locations):
            if not i:
                loc = item.replace(' ', '+')
                loc = urllib.parse.quote(loc, safe='+')
                url += loc.lower()
            else:
                # wollstonecraft%2c+nsw+2065%3b+waverton%2c+nsw+2060%3b+
                loc = item.replace(' ', '+')
                loc = urllib.parse.quote(loc, safe='+')
                url += "%3b+{}".format(loc.lower())

            if len(self.locations) > 1 and i == len(self.locations) - 1:
                url += "%3b+"

        url += "/list-1?source=location-search"

        return url


    def domain_url(self):
        """Creates a url for domain.com.au searches"""
        raise NotImplementedError

    def get_page(self, url):
        """Given a url, will return the HTML of a page"""
        # use loop logic outside of a function, not here

    def get_all_listings(self, html):
        """Given html, will retun a list of all object listings """
        # 20 to a page?
        pass

        

#####################
#
#####################




origin = 'the property address'
nine_am = ''  # integer epoch timestamp of wednesday 9am. Needs time logic

# call for Rhys

# destination = secrets.rhys_work

# result = gmaps.distance_matrix(origin,
#                                destination,
#                                mode='transit',
#                                language='en-AU',
#                                units='metric',
#                                arrival_time=nine_am)

# returns:
# {'destination_addresses': ['secret destination'], 'origin_addresses': ['secret origin'], 'rows': [{'elements': [{'distance': {'text': '5.9 km', 'value': 5918}, 'duration': {'text': '26 mins', 'value': 1568}, 'status': 'OK'}]}], 'status': 'OK'}


# call for Kristen

# destination = secrets.kristen_work

# result = gmaps.distance_matrix(origin,
#                                destination,
#                                mode='driving',
#                                language='en-AU',
#                                units='metric',
#                                arrival_time=nine_am)

# returns:
# {'destination_addresses': ['secret destination'], 'origin_addresses': ['secret origin'], 'rows': [{'elements': [{'distance': {'text': '16.1 km', 'value': 16096}, 'duration': {'text': '19 mins', 'value': 1116}, 'status': 'OK'}]}], 'status': 'OK'}

#########
# scraper stuff
#########

# example url. Modify to include regions?
# https://www.realestate.com.au/rent/property-townhouse-house-with-studio-between-0-1100-in-crows+nest%2c+nsw+2065%3b+wollstonecraft%2c+nsw+2065/list-1?numBaths=2&maxBeds=3&source=location-search


if __name__ == '__main__':
    pass