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

gmaps = googlemaps.Client(key=secrets.matrix_api_key)

suburb_list = []


#####################
# Search class
#####################

class HouseType():
    """docstring for ClassName"""
    def __init__(self):
        self.num_bedrooms = None
        self.num_bathrooms = None
        self.some_other_param = None
        self.listing_results = []  # a list of objects that are successfull matches

    def realestate_url(self):
        """Creates a url to use with realestate.com.au searches"""
        pass

    def domain_url(self):
        """Creates a url for domain.com.au searches"""
        pass



        

#####################
#
#####################




origin = 'the property address'
nine_am = ''  # integer epoch timestamp of wednesday 9am. Needs time logic

# call for Rhys

destination = secrets.rhys_work

result = gmaps.distance_matrix(origin,
                               destination,
                               mode='transit',
                               language='en-AU',
                               units='metric',
                               arrival_time=nine_am)

# returns:
# {'destination_addresses': ['secret destination'], 'origin_addresses': ['secret origin'], 'rows': [{'elements': [{'distance': {'text': '5.9 km', 'value': 5918}, 'duration': {'text': '26 mins', 'value': 1568}, 'status': 'OK'}]}], 'status': 'OK'}


# call for Kristen

destination = secrets.kristen_work

result = gmaps.distance_matrix(origin,
                               destination,
                               mode='driving',
                               language='en-AU',
                               units='metric',
                               arrival_time=nine_am)

# returns:
# {'destination_addresses': ['secret destination'], 'origin_addresses': ['secret origin'], 'rows': [{'elements': [{'distance': {'text': '16.1 km', 'value': 16096}, 'duration': {'text': '19 mins', 'value': 1116}, 'status': 'OK'}]}], 'status': 'OK'}

#########
# scraper stuff
#########

# example url. Modify to include regions?
# https://www.realestate.com.au/rent/property-townhouse-house-with-studio-between-0-1100-in-crows+nest%2c+nsw+2065%3b+wollstonecraft%2c+nsw+2065/list-1?numBaths=2&maxBeds=3&source=location-search




