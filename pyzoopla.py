_zkey = “ADD KEY HERE” # get from http://developer.zoopla.com/home
import requests
import json


_error_codes = {400: "Bad Request",
                401: "Unautorised",
                403: "Forbidden",
                404: "Not Found",
                405: "Method Not Allowed",
                500: "Internal Server Error"}


def format_response(zoopla_function):
    """
    Basic decorator to convert output of Zoopla function into a json file and
    process any errors found
    """
    def inner(postcode, **specific_args):
        response = zoopla_function(postcode, **specific_args)
        assert response.status_code == 200, _error_codes.get(response.status_code, "Unknown Error")
        response = json.loads(response.text)
        if "error_string" in response:
            raise Exception(response["error_string"])
        else:
            return response
    return inner


def basic_zoopla_function(command, postcode, **optional_args):
    """generic zoopla function"""
    opt_args = "".join(["&"+option+"="+str(setting) for option, setting in optional_args.items()])
    httproot = "http://api.zoopla.co.uk/api/v1/"+command+".js?"
    query = httproot+"postcode="+postcode+opt_args+"&output_type=outcode&api_key="+_zkey
    return requests.get(query)


@format_response
def z_index(postcode):
    """
    Return Parameters
    area_url	        A fully qualified URL pointing to the returned Zed Index! on the www.zoopla.co.uk Web site
    zed_index	        Most recent Zed-Index! for the area requested.
    zed_index_3month	Zed-Index! as of 3 months ago.
    zed_index_6month	Zed-Index! as of 6 months ago.
    zed_index_1year	    Zed-Index! as of 1 year ago.
    zed_index_2year	    Zed-Index! as of 2 year ago.
    zed_index_3year	    Zed-Index! as of 3 years ago.
    zed_index_4year	    Zed-Index! as of 4 years ago.
    zed_index_5year	    Zed-Index! as of 5 years ago.
    """
    return basic_zoopla_function("zed_index", postcode)


@format_response
def avg_sold_price(postcode):
    """
    Return Paramters
    name	                    Name associated with the type of output list request, e.g. requesting "streets" may
                                produce "Downing Street".
    average_sold_price_1year	The average sale price for the requested area within the last year.
    average_sold_price_3year	The average sale price for the requested area within the 3 years.
    average_sold_price_5year	The average sale price for the requested area within the 5 years.
    average_sold_price_7year	The average sale price for the requested area within the 7 years.
    number_of_sales_1year	    Number of property sales in the requested area within the last year.
    number_of_sales_3year	    Number of property sales in the requested area within the 3 years.
    number_of_sales_5year	    Number of property sales in the requested area within the 5 years.
    number_of_sales_7year	    Number of property sales in the requested area within the 7 years.
    turnover	                Percentage turnover for the requested area. The Turnover is calculated by dividing the
                                number of sales over the last 5 years (excluding new build properties) by the number
                                of homes in a given area.
    prices_url	                A link to the appropriate sold prices page on www.zoopla.co.uk
    """
    return basic_zoopla_function("average_area_sold_price", postcode)


@format_response
def property_listings(postcode, radius=0.5,
                                order_by="price",
                                ordering="descending",
                                listing_status="sale",
                                include_sold=1,
                                minimum_price=0,
                                maximum_price=2000000,
                                minimum_beds=0,
                                maximum_beds=5,
                                property_type="flats",
                                new_homes="false",
                                chain_free="false",
                                keywords="",
                                page_number=1,
                                page_size=10,
                                summarised="true"
                                               ):
    """
    radius	            When providing a latitude and longitude position, this is the radius from the position to find
                        listings. Default value is 0.5 miles, maximum radius is 40 miles.
    order_by	        The value which the results should be ordered, either "price" (default) or "age" of listing.
    ordering	        Sort order for the listings returned. Either "descending" (default) or "ascending".
    listing_status	    Request a specific listing status. Either "sale" or "rent".
    include_sold	    Whether to include property listings that are already sold in the results when searching for
                        sale listings, either "1" or "0". Defaults to 0.
    include_rented	    Whether to include property listings that are already rented in the results when searching for
                        rental listings, either "1" or "0". Defaults to 0.
    minimum_price	    Minimum price for the property, in GBP. When listing_status is "sale" this refers to the sale
                        price and when listing_status is "rent" it refers to the per-week price.
    maximum_price	    Maximum price for the property, in GBP.
    minimum_beds	    The minimum number of bedrooms the property should have.
    maximum_beds	    The maximum number of bedrooms the property should have.
                        This parameter only applies to searches related to rental property.
    property_type	    Type of property, either "houses" or "flats".
    new_homes	        Specifying "yes"/"true" will restrict to only new homes, "no"/"false" will exclude them from
                        the results set.
    chain_free	        Specifying "yes"/"true" will restrict to chain free homes, "no"/"false" will exclude them from
                        the results set.
    keywords	        Keywords to search for within the listing description.
    page_number	        The page number of results to request, default 1.
    page_size	        The size of each page of results, default 10, maximum 100.
    summarised	        Specifying "yes"/"true" will return a cut-down entry for each listing with the description
                        cut short and the following fields will be removed: price_change, floor_plan.

    """
    return basic_zoopla_function("property_listings", **locals())






