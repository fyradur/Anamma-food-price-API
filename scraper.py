from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re

# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# current directory
chrome_driver = "./resources/chromedriver_linux64/chromedriver"

# go to Google and click the I'm Feeling Lucky button
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.get("https://www.matspar.se/produkt/vegofars-1000-g")
#lucky_button = driver.find_element_by_css_selector("[name=btnI]")
#lucky_button.click()

store_divs = driver.find_elements_by_class_name("_2qyvs")
store1 = store_divs[0]
store4 = store_divs[3]


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

print(f"Amount of stores: {len(store_divs)}")
print(f"Fourth store inner text: {store4.text}")
print(f"Fourth store inner html: {store4.get_attribute('innerHTML')}")
print(f"Fourth store name: {get_store_name_from_div(store4)}")
print(f"First store price: {get_price_from_div(store1)}")
print(f"The scraped product: {scrape_product(driver)}")

# capture the screen
#driver.get_screenshot_as_file("capture.png")
