import requests
import re
import yaml
import logging
import smtplib
import json

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup as soup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def load_properties(yaml_path):
    '''
    Load properties from yaml file
    '''
    logging.info("Loading URLs started")
    with open(yaml_path, 'r') as file:
        try:
            yaml_dict = yaml.safe_load(file)
            logging.info("Yaml file successfully loaded")

            if 'src_email_addr' not in yaml_dict or len(yaml_dict['src_email_addr']) == 0:
                logging.error("Yaml config does not contain source email address")
                return False

            if 'src_email_passwd' not in yaml_dict or len(yaml_dict['src_email_passwd']) == 0:
                logging.error("Yaml config does not contain email password")
                return False

            if 'urls' not in yaml_dict or len(yaml_dict['urls']) == 0:
                logging.error("Yaml config does not contain any URLs or urls section")
                return False

            if 'dest_email' not in yaml_dict or len(yaml_dict['dest_email']) == 0:
                logging.error("Yaml config does not contain destination email address")
                return False

            return yaml_dict

        except yaml.YAMLError as exc:
            logging.error("Failed to load yaml file", str(exc))
            return False

def scrape_http_data(url):
    '''
    Scrape data from otomoto website
    '''
    cars_list = dict()

    webpage = requests.get(url)
    webpage_parsed = soup(webpage.content, 'html.parser')

    error_message = webpage_parsed.find_all("div", {"data-testid": "message-container"})
    if error_message:
        logging.info(f'No cars found in URL: {url}')
        return False

    search_results = webpage_parsed.find_all("article", {"data-testid": "listing-ad"})

    if len(search_results) == 0:
        raise Exception("Webpage has not loaded correctly")

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
        if price_info.findChildren("div"):
            car['car_otomoto_rating'] = price_info.find_next("div").find_next("p").get_text()
        else:
            car['car_otomoto_rating'] = ""

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

def analyze_data(cars_list, is_hourly):
    '''
    Analyze data and update results
    '''
    logging.info(f'Analyzing data started. Daily is set to {str(is_hourly)}')
    final_dict = {
        'new': {},
        'available': {},
        'gone': {}
    }

    if is_hourly:
        result_path = 'results/hourly.json'
    else:
        result_path = 'results/daily.json'

    with open(result_path, 'r') as previous_file:
        previous_json = previous_file.read()
        if previous_json:
            # File is not empty
            logging.info(f'Cars found in result json.')
            previous_results = json.loads(previous_json)

            for car in cars_list:
                if car in previous_results['new'] or car in previous_results['available'] or car in previous_results['gone']:
                    # Car that was already available before
                    logging.debug(f'Car already available - {cars_list[car]["car_name"]}')
                    final_dict['available'][car] = cars_list[car]
                else:
                    # New car
                    logging.debug(f'New car found - {cars_list[car]["car_name"]}')
                    final_dict['new'][car] = cars_list[car]
            
            for previous_car in previous_results['new'].keys():
                if previous_car not in cars_list.keys():
                    # Car that is not available now, but was before
                    logging.info(f'Car is gone - {previous_car}')
                    final_dict['gone'][previous_car] = previous_results['new'][previous_car]
            for previous_car in previous_results['available'].keys():
                if previous_car not in cars_list.keys():
                    # Car that is not available now, but was before
                    logging.info(f'Car is gone - {previous_car}')
                    final_dict['gone'][previous_car] = previous_results['available'][previous_car]

        else:
            # Empty file - add every car to 'new' section
            logging.info(f'No cars found in result json.')
            for car in cars_list:
                final_dict['new'][car] = cars_list[car]

    try:
        with open(result_path, "w") as file:
            file.write(json.dumps(final_dict))
    except Exception as exc:
        logging.error("Failed to save results to file, ", str(exc))
        return False


    logging.info('Analyzing data finished successfully.')
    logging.info(f'Analyzing data statistics: New = {len(final_dict["new"])}, \
                   Available = {len(final_dict["available"])}, Gone = {len(final_dict["gone"])}.')
    
    return final_dict

def render_email(search_resaults):
    '''
    Render html email from given search results
    '''
    try:
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('email_template.html')
        template_rendered = template.render(cars = search_resaults)
        logging.info("Email successfully rendered")
        return template_rendered

    except Exception as exc:
        logging.error("Failed to render email. Error: ", str(exc))
        return False

def send_email(src_address, src_passwd, dest_address, is_hourly, mail_content):
    '''
    Send html email
    '''
    message = MIMEMultipart()
    message['From'] = src_address
    message['To'] = dest_address
    if is_hourly:
        message['Subject'] = 'Otomoto Notifier - update'
    else:
        message['Subject'] = 'Otomoto Notifier - Daily update'
    logging.info(f"Sending email to {dest_address}.")

    try:
        message.attach(MIMEText(mail_content, 'html'))
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(src_address, src_passwd)
        text = message.as_string()
        session.sendmail(src_address, dest_address, text)
        session.quit()

    except Exception as exc:
        logging.error("Failed to send email. Error: ", str(exc))
        return False

    logging.info("Email successfully sent.")
    return True
