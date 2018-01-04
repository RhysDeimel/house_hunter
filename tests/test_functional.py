import house_hunter as hh

def test_get_page_returns_string():
    # in here because am not stubbing a requests interface
     prop = hh.HouseType()
     expected = prop.get_page("https://www.realestate.com.au/rent/list-1")
     assert type(expected) == str