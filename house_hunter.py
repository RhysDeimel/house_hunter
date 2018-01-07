import googlemaps
import secrets
import urllib.parse
import requests
import re
import time
import pygsheets
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
        url = "https://www.realestate.com.au/rent/property-townhouse-house-between-0-1100-in-"
        for i, item in enumerate(self.locations):
            if not i:
                loc = item.replace(' ', '+')
                loc = urllib.parse.quote(loc, safe='+')
                url += loc.lower()
            else:
                loc = item.replace(' ', '+')
                loc = urllib.parse.quote(loc, safe='+')
                url += "%3b+{}".format(loc.lower())

            if len(self.locations) > 1 and i == len(self.locations) - 1:
                url += "%3b+"

        url += "/list-0?source=location-search"

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
        listings = []
        soup = BeautifulSoup(html, 'html.parser')

        page_listings = soup.find_all("div", class_="listingInfo")

        for item in page_listings:

            address = item.find("a")

            try:
                price = item.find("p", class_="priceText")
                price = price.text
                pattern = re.compile("(\d,\d+)|(\d+)")
                re_result = pattern.search(price)
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

            listing = {
                'address': address.text,
                'price': price,
                'bed': details[0],
                'bath': details[1],
                'car': details[2],
                'url': address.get('href'),
                'distance_kristen': None,
                'distance_rhys': None
            }

            listings.append(listing)

        return listings

    def filter_by_price_and_bath(self, listings):
        print("Filtering listings by price and bathrooms")
        filtered_list = []

        for item in listings:
            if 0 < item["price"] > 1100:
                continue
            elif item["bath"] < 2:
                continue
            else:
                filtered_list.append(item)

        return filtered_list

    def calculate_travel_time(self, listings):
        for item in listings:
            print("Calculating travel times for {}".format(item['address']))
            item['distance_kristen'] = self.check_distance(secrets.kristen_work,
                                                           item['address'],
                                                           'driving')

            item['distance_rhys'] = self.check_distance(secrets.rhys_work,
                                                        item['address'],
                                                        'transit')
        return listings

    def check_distance(self, origin, destination, mode):
        result = self.gmaps.distance_matrix(origin,
                                            destination,
                                            mode=mode,
                                            language='en-AU',
                                            units='metric',
                                            arrival_time=self.nine_am)
        try:
            return result['rows'][0]['elements'][0]['duration']['value']
        except KeyError:
            return 0


    def filter_times(self, listings):
        print("Filtering listings by travel times")
        filtered_list = []

        for item in listings:
            if item["distance_kristen"] // 60 > 60:
                continue
            elif item["distance_rhys"] // 60 > 60:
                continue
            else:
                filtered_list.append(item)

        return filtered_list


    def get_sheet(self):
        print("Getting google sheet")
        gc = pygsheets.authorize()
        sh = gc.open('PropertyHunt')
        wks = sh.sheet1
        return wks

    def filter_from_gsheet_entries(self, gsheet, listings):
        print("Filtering listings from the google sheet")
        filtered_list = []
        previously_found_properties = gsheet.get_col(1, include_empty=False)
        for item in listings:
            if not item['address'] in previously_found_properties:
                filtered_list.append(item)

        return filtered_list

    def write_to_sheet(self, gsheet, listings):
        listing_matrix = []

        for item in listings:
            print("Adding to matrix: {}".format(item['address']))
            listing = []
            listing.append(item['address'])
            listing.append("${}".format(item['price']))
            listing.append(item['bed'])
            listing.append(item['bath'])
            listing.append(item['car'])
            listing.append("{} mins".format(item['distance_kristen'] // 60))
            listing.append("{} mins".format(item['distance_rhys'] // 60))
            listing.append("https://www.realestate.com.au{}".format(item['url']))
            listing_matrix.append(listing)

        if listing_matrix:
            print("Batch updating sheet")
            gsheet.insert_rows(1, number=len(listing_matrix), values=listing_matrix)
        else:
            print("Nothing to update")


if __name__ == '__main__':
    prop = HouseType(locations=suburb_list,
                     property_type=["townhouse",
                                    "house"])
    url = prop.realestate_url()
    
    count = 0
    listings = []
    while True:
        url = url.replace('list-{}'.format(count), 'list-{}'.format(count + 1))

        print("Getting page {}".format(count + 1))
        page = prop.get_page(url)
        print("Getting page {} listings".format(count + 1))
        results = prop.get_all_listings(page)

        if not results:
            break
        listings += results
        count += 1
        time.sleep(3)

    feature_filtered = prop.filter_by_price_and_bath(listings)

    gsheet = prop.get_sheet()
    new_listings = prop.filter_from_gsheet_entries(gsheet, feature_filtered)

    times_added = prop.calculate_travel_time(new_listings)
    prop.listing_results = prop.filter_times(times_added)

    prop.write_to_sheet(gsheet, prop.listing_results)
    print("Finished!")