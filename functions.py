import requests
import re
import yaml
import logging
from bs4 import BeautifulSoup as soup

def load_urls(url_path):
    logging.info("Loading URLs started")
    with open(url_path, 'r') as file:
        try:
            urls_yaml = yaml.safe_load(file)
            logging.info("Loading URLs finished successfully")

            if 'urls' in urls_yaml and len(urls_yaml['urls']):
                return urls_yaml['urls']

            logging.error("File does not contain any URLs or urls section", exc)
            return False

        except yaml.YAMLError as exc:
            logging.error("Failed to load URLs", exc)
            return False

def http_parser(url):
    webpage = requests.get(url)
    webpage_parsed = soup(webpage.content, 'html.parser')

    error_message = webpage_parsed.find_all("div", {"data-testid": "message-container"})
    if error_message:
        return False

    search_results = webpage_parsed.find_all("article", {"data-testid": "listing-ad"})

    for result in search_results:
        data = result.find_next("div")
        primary_info = data.find_next("h2").find_next("a")
        car_name = primary_info.get_text()
        car_url = primary_info['href']

        details = data.find_next("div").find_next("ul").find_all("li")
        car_year = details[0].get_text().strip()
        car_distance = details[1].get_text()
        car_engine_cap = details[2].get_text()
        car_engine_type = details[3].get_text()

        car_location = data.find_all("p")[-1].get_text()

        price_info = result.find_all("div")[3]
        car_price = price_info.find_next("span").get_text()
        car_otomoto_rating = price_info.find_next("div").find_next("p").get_text()

        car_webpage_parsed = soup(requests.get(car_url).content, 'html.parser')
        car_params = car_webpage_parsed.find_all("li", {"class": "offer-params__item"})
        car_engine_power = None
        for param in car_params:
            if re.match("^[0-9]+ KM$", param.find_next("div").get_text().strip()):
                car_engine_power = param.find_next("div").get_text().strip()

        logging.info(f'Searched car: name: {car_name}, year: {car_year}, price: {car_price}, pow: {car_engine_power}')

def email_sender():
    pass