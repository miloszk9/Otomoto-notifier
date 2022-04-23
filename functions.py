import requests
import re
import yaml
import logging
import smtplib

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup as soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def load_properties(yaml_path):
    logging.info("Loading URLs started")
    with open(yaml_path, 'r') as file:
        try:
            yaml_dict = yaml.safe_load(file)
            logging.info("Yaml file successfully loaded")

            if 'urls' not in yaml_dict or len(yaml_dict['urls']) == 0:
                logging.error("Yaml config does not contain any URLs or urls section")
                return False

            if 'dest_email' not in yaml_dict or len(yaml_dict['dest_email']) == 0:
                logging.error("Yaml config does not contain email address")
                return False

            return yaml_dict

        except yaml.YAMLError as exc:
            logging.error("Failed to load yaml file", exc)
            return False

def parse_html(url):
    cars_list = dict()

    webpage = requests.get(url)
    webpage_parsed = soup(webpage.content, 'html.parser')

    error_message = webpage_parsed.find_all("div", {"data-testid": "message-container"})
    if error_message:
        logging.info(f'No cars found in URL: {url}')
        return False

    search_results = webpage_parsed.find_all("article", {"data-testid": "listing-ad"})

    for result in search_results:
        car = dict()

        data = result.find_next("div")
        primary_info = data.find_next("h2").find_next("a")
        car['car_name'] = primary_info.get_text()
        car['car_url'] = primary_info['href']

        details = data.find_next("div").find_next("ul").find_all("li")
        car['car_year'] = details[0].get_text().strip()
        car['car_distance'] = details[1].get_text()
        car['car_engine_cap'] = details[2].get_text()
        car['car_engine_type'] = details[3].get_text()

        car['car_location'] = data.find_all("p")[-1].get_text()

        image_div = result.find_all("div")[2]
        image_section = image_div.find_next("span").find_next("img")
        car['car_image_url'] = image_section['src']

        price_info = result.find_all("div")[3]
        car['car_price'] = price_info.find_next("span").get_text()
        car['car_otomoto_rating'] = price_info.find_next("div").find_next("p").get_text()

        car_webpage_parsed = soup(requests.get(primary_info['href']).content, 'html.parser')
        car_params = car_webpage_parsed.find_all("li", {"class": "offer-params__item"})
        car_engine_power = None
        for param in car_params:
            if re.match("^[0-9]+ KM$", param.find_next("div").get_text().strip()):
                car['car_engine_power'] = param.find_next("div").get_text().strip()

        logging.info(f"Searched car: name: {car['car_name']}, year: {car['car_year']},\
                     price: {car['car_price']}, pow: {car['car_engine_power']},\
                     img url: {car['car_image_url']}")

        cars_list[primary_info['href']] = car
        
    return cars_list

def render_email(search_resaults):
    try:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('email_template.html')
        template_rendered = template.render(cars = search_resaults)
        logging.info("Email successfully rendered")
        return template_rendered

    except Exception as exc:
        logging.error("Failed to render email. Error: ", str(exc))
        return False

def send_email(src_address, src_passwd, dest_address):
    pass
