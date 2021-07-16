from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import json
import flask
from flask import request

app = flask.Flask(__name__)

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("disable-infobars") # disabling infobars
chrome_options.add_argument("--disable-extensions") # disabling extensions
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
chrome_options.add_argument("--no-sandbox") #Bypass OS security model

chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#chrome_driver = "./resources/chromedriver_linux64/chromedriver"
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)


def get_store_name_from_div(div):
    """ Pass in the div and get the name of the store."""
    div_text = div.get_attribute('innerHTML')
    store_with_suffix_and_prefix = re.search("logos\/.*\.svg", div_text).group()
    store_with_suffix = store_with_suffix_and_prefix[6:]
    store = re.sub("\..*\.svg", "",
                   store_with_suffix,
                   1)
    return store


def get_price_from_div(div):
    """ Pass in the div and get the price."""
    price_div = div.find_element_by_class_name('_3n8y8')
    price_div_text = price_div.get_attribute('innerHTML')
    price = re.search("\d*,\d*", price_div_text).group()
    price_english_form_as_string = re.sub(",", ".",
                                          price,
                                          1)
    price_as_float = float(price_english_form_as_string)
    return price_as_float


def scrape_product(driver):
    """ Given that the selenium driver object is at a valid product page,
    this function will return a dictionary with the keys being stores and
    the values being the corresponding price.
    """
    stores = driver.find_elements_by_class_name("_2qyvs") 
    result = {get_store_name_from_div(store) : get_price_from_div(store)
              for store in stores}
    return result


def scrape_page(product):
    """ Given the product, this scrapes the corresponding page and
    returns a json where the keys are stores and the values are
    the corresponding prices.
    """
    if product == "vegofars":
        driver.get("https://www.matspar.se/produkt/vegofars-1000-g")
        return json.dumps(scrape_product(driver))
    elif product == "vegokorv":
        driver.get("https://www.matspar.se/produkt/vegokorv-840-g")
        return json.dumps(scrape_product(driver))
    elif product == "vegobullar":
        driver.get("https://www.matspar.se/produkt/vegobullar-900-g")
        return json.dumps(scrape_product(driver))
    elif product == "vegopizza":
        driver.get("https://www.matspar.se/produkt/vegocapricciosa-350g-anamma")
        return json.dumps(scrape_product(driver))
    elif product == "vegodip":
        driver.get("https://www.matspar.se/produkt/vegan-ch-se-dip-240g-frankful")
        return json.dumps(scrape_product(driver))



@app.route('/', methods=['GET'])
def get_prices():
    food = request.args['food']
    try:
        return scrape_page(food)
    except:
        return "something went wrong"


#print(f"The scraped product: {scrape_page('vegodip')}")
