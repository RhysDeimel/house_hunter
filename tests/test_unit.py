import pytest
import house_hunter as hh


class Test_realestate_url():

    def test_search_with_one_location(self):
        prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"],
                            property_type=["townhouse",
                                           "unit and apartment",
                                           "house"])
        expected = "https://www.realestate.com.au/rent/property-townhouse-unit+apartment-house-between-0-1100-in-wollstonecraft%2c+nsw+2065/list-1?source=location-search"
        assert prop.realestate_url() == expected

    def test_search_with_two_locations(self):
        prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",
                                       "Waverton, NSW 2060"],
                            property_type=["townhouse",
                                           "unit and apartment",
                                           "house"])
        expected = "https://www.realestate.com.au/rent/property-townhouse-unit+apartment-house-between-0-1100-in-wollstonecraft%2c+nsw+2065%3b+waverton%2c+nsw+2060%3b+/list-1?source=location-search"
        assert prop.realestate_url() == expected

    def test_search_with_three_locations(self):
        prop = hh.HouseType(locations=["Lavender Bay, NSW 2060",
                                       "Cremorne, NSW 2090",
                                       "Manly, NSW 2095"],
                            property_type=["townhouse",
                                           "unit and apartment",
                                           "house"])
        expected = "https://www.realestate.com.au/rent/property-townhouse-unit+apartment-house-between-0-1100-in-lavender+bay%2c+nsw+2060%3b+cremorne%2c+nsw+2090%3b+manly%2c+nsw+2095%3b+/list-1?source=location-search"
        assert prop.realestate_url() == expected

    def test_get_all_listings_returns_20_items(self):
        prop = hh.HouseType()

        with open("tests/page1.html") as page:
            given = prop.get_all_listings(page.read())

        assert len(given) == 20

    # Time pressures, deal with this crap later
    #######################
    # def test_HouseType_with_all_none(self):
    #     prop = hh.HouseType()
    #     expected = "https://www.realestate.com.au/rent/list-1"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_only():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"])
    #     expected = "https://www.realestate.com.au/rent/in-wollstonecraft%2c+nsw+2065%3b+/list-1?source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_single_suburb_and_single_property():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], property_type=["house"])
    #     expected = "https://www.realestate.com.au/rent/property-house-in-wollstonecraft%2c+nsw+2065/list-1?source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_multiple_suburb_and_multiple_prop():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065", "Waverton, NSW 2060", "St Leonards, NSW 2065"],
    #                         property_type=["house", "apartment & unit", "townhouse"])
    #     expected = "https://www.realestate.com.au/rent/property-townhouse-unit+apartment-house-in-wollstonecraft%2c+nsw+2065%3b+waverton%2c+nsw+2060%3b+st+leonards%2c+nsw+2065%3b+/list-1?source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_min_beds():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], min_beds=2)
    #     expected = "https://www.realestate.com.au/rent/with-2-bedrooms-in-wollstonecraft%2c+nsw+2065%3b/list-1?maxBeds=any&source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_max_beds():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], max_beds=4)
    #     expected = "https://www.realestate.com.au/rent/with-studio-in-wollstonecraft%2c+nsw+2065/list-1?maxBeds=4&source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_min_and_max_beds():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], min_beds=1,
    #                         max_beds=4)
    #     expected = "https://www.realestate.com.au/rent/with-1-bedroom-in-wollstonecraft%2c+nsw+2065/list-1?maxBeds=4&source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_min_price():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], min_price=500)
    #     expected = "https://www.realestate.com.au/rent/between-500-any-in-wollstonecraft%2c+nsw+2065/list-1?source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_max_price():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], max_price=1100)
    #     expected = "https://www.realestate.com.au/rent/between-0-1100-in-wollstonecraft%2c+nsw+2065/list-1?source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_min_and_max_price():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], min_price=550,
    #                         max_price=1100)
    #     expected = "https://www.realestate.com.au/rent/between-550-1200-in-wollstonecraft%2c+nsw+2065/list-1?source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_bathrooms():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], bathrooms=2)
    #     expected = "https://www.realestate.com.au/rent/in-wollstonecraft%2c+nsw+2065/list-1?numBaths=2&source=location-search"
    #     assert prop.realestate_url() == expected

    # def test_HouseType_with_suburb_and_car_spaces():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",], car_spaces=2)
    #     expected = "https://www.realestate.com.au/rent/in-wollstonecraft%2c+nsw+2065/list-1?numParkingSpaces=2&source=location-search"
    #     assert prop.realestate_url() == expected 

    # def test_HouseType_with_all_params():
    #     prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065",
    #                                    "Waverton, NSW 2060",
    #                                    "St Leonards, NSW 2065"],
    #                         property_type=["house", "apartment & unit", "townhouse",
    #                                        "villa", "acreage", "block of units",
    #                                        "retirement living"],
    #                         min_beds=1, max_beds=5, min_price=50, max_price=5000,
    #                         bathrooms=1, car_spaces=1)
    #     expected = "https://www.realestate.com.au/rent/property-retire-unitblock-acreage-villa-townhouse-unit+apartment-house-with-1-bedroom-between-50-5000-in-wollstonecraft%2c+nsw+2065%3b+waverton%2c+nsw+2060%3b+st+leonards%2c+nsw+2065%3b+/list-1?numParkingSpaces=1&numBaths=1&maxBeds=5&source=location-search"
    #     assert prop.realestate_url() == expected 


    # def test_HouseType_catches_invalid_property_type():
    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], property_type=["asdf"])

    # def test_HouseType_prices_less_than_750_increment_by_25():
    #     # starts at 50
    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], min_price=12)

    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], max_price=749)

    # def test_HouseType_prices_greater_than_750_and_less_than_1000_increment_by_50():
    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], min_price=799)

    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], max_price=925)

    # def test_HouseType_prices_between_1000_and_2000_increment_by_100():
    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], min_price=1099)

    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], max_price=1950)

    # def test_HouseType_prices_greater_than_2000_increment_by_500():
    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], min_price=2025)

    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], max_price=4550)

    # def test_HouseType_prices_max_is_5000():
    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], max_price=5001)

    #     with pytest.raises(Exception) as e_info:
    #         prop = hh.HouseType(locations=["Wollstonecraft, NSW 2065"], max_price=5025)
