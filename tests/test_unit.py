import house_hunter as hh

def test_HouseType_with_all_none():
	no_req_prop = hh.HouseType()
	expected = "https://www.realestate.com.au/rent/list-1"
	assert no_req_prop.realestate_url() == expected