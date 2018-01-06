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
import re
from bs4 import BeautifulSoup



suburb_list = ["Wollstonecraft, NSW 2065"]


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
        self.gmaps = googlemaps.Client(key=secrets.matrix_api_key)
        self.nine_am = 1515226851

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
        r = requests.get(url)
        return r.text

    def get_all_listings(self, html):
        """Given html, will retun a list of all object listings """
        # 20 to a page?
        listings = []
        soup = BeautifulSoup(html, 'html.parser')

        page_listings = soup.find_all("div", class_="listingInfo")

        for item in page_listings:

            address = item.find("a")

            # search in page listing[0]
            price = item.find("p", class_="priceText")
            price = price.text
            pattern = re.compile("(\d,\d+)|(\d+)")
            re_result = pattern.search(price)
            try:
                price = re_result.group()
                price = price.replace(",", "")
                price = int(price)
            except AttributeError:
                price = 0

            property_features = item.find("dl", class_="rui-property-features")
            property_features = property_features.find_all("dd")
            details = []
            for i in range(3):
                try:
                    details.append(int(property_features[i].text))
                except IndexError:
                    details.append(0)

            distance_kristen = self.check_distance(secrets.kristen_work,
                                                   address.text,
                                                   'driving')
            distance_rhys = self.check_distance(secrets.rhys_work,
                                                address.text,
                                                'transit')

            listing = {
                'address': address.text,
                'price': price,
                'bed': details[0],
                'bath': details[1],
                'car': details[2],
                'url': address.get('href'),
                'distance_kristen': distance_kristen,
                'distance_rhys': distance_rhys
            }

            listings.append(listing)

        print(listings)
        return listings

    def filter_listings(self, listings):
        for item in listings:
            if item["price"] > 1100:
                continue
            elif item["bath"] == 1:
                continue
            # 60min for Kristen and I
            elif item["distance_kristen"] // 60 > 60:
                continue
            elif item["distance_rhys"] // 60 > 60:
                continue
            else:
                self.listing_results.append(item)

    def check_distance(self, origin, destination, mode):
        result = self.gmaps.distance_matrix(origin,
                                            destination,
                                            mode=mode,
                                            language='en-AU',
                                            units='metric',
                                            arrival_time=self.nine_am)

        return result['rows'][0]['elements'][0]['duration']['value']

# {
#    'destination_addresses':[
#       'secret destination'
#    ],
#    'origin_addresses':[
#       'secret origin'
#    ],
#    'rows':[
#       {
#          'elements':[
#             {
#                'distance':{
#                   'text':'5.9 km',
#                   'value':5918
#                },
#                'duration':{
#                   'text':'26 mins',
#                   'value':1568
#                },
#                'status':'OK'
#             }
#          ]
#       }
#    ],
#    'status':'OK'
# }



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
    prop = HouseType(locations=suburb_list,
                     property_type=["townhouse",
                                    "house"])
    url = prop.realestate_url()
    prop.filter_listings(prop.get_all_listings(prop.get_page(url)))
    print(prop.listing_results)
