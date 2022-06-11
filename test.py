import os
import json
from time import sleep
from random import random
from functions import *

def test_load_properties():
    dirname = os.path.dirname(__file__)
    yaml_dict = load_properties(os.path.join(dirname, 'volume/config.yml'))
    return yaml_dict

def test_render_email():
    cars = {
        'new':{
            'car1_url_uniq': {
                'car_url': 'https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InE5b3dkdWtmZzcwNDMtT1RPTU9UT1BMIiwidyI6W3siZm4iOiJ3ZzRnbnFwNnkxZi1PVE9NT1RPUEwiLCJzIjoiMTYiLCJwIjoiMTAsLTEwIiwiYSI6IjAifV19.nD77DguP9rXwmf4t_6lyNLVh15ouXUceXJqMK8KFI2U/image;s=320x240',
                'car_name': 'Foo',
                'car_year': 2137,
                'car_distance': 20000,
                'car_location': 'test',
                'car_engine_type': 'test1',
                'car_engine_cap': 'car_engine_cap',
                'car_engine_power': 'car_engine_power',
                'car_price': 'car_price',
                'car_otomoto_rating': 'car_otomoto_rating'
            }
        },
        'available':{
            'car2_url_uniq': {
                'car_url': 'https://ireland.apollo.olxcdn.com/v1/files/eyJmbiI6InE5b3dkdWtmZzcwNDMtT1RPTU9UT1BMIiwidyI6W3siZm4iOiJ3ZzRnbnFwNnkxZi1PVE9NT1RPUEwiLCJzIjoiMTYiLCJwIjoiMTAsLTEwIiwiYSI6IjAifV19.nD77DguP9rXwmf4t_6lyNLVh15ouXUceXJqMK8KFI2U/image;s=320x240',
                'car_name': 'Foo',
                'car_year': 2137,
                'car_distance': 20000,
                'car_location': 'test',
                'car_engine_type': 'test1',
                'car_engine_cap': 'car_engine_cap',
                'car_engine_power': 'car_engine_power',
                'car_price': 'car_price',
                'car_otomoto_rating': 'car_otomoto_rating'
            }
        },
        'gone':{}
    }
    dirname = os.path.dirname(__file__)
    render = render_email(cars, dirname)
    # with open("out.html", "w") as file:
    #     file.write(render)

    return render

def test_scrape_http_data():
    url = 'https://www.otomoto.pl/osobowe/renault/megane/seg-city-car--seg-coupe/od-2008/podkarpackie?search%5Bfilter_enum_generation%5D=gen-iii-2008-2016&search%5Bfilter_float_year%3Ato%5D=2013&search%5Bfilter_float_mileage%3Ato%5D=240000&search%5Bfilter_float_price%3Afrom%5D=13000&search%5Bfilter_float_price%3Ato%5D=20000&search%5Border%5D=created_at_first%3Adesc&search%5Badvanced_search_expanded%5D=true'
    result_json = scrape_http_data(url)
    print(result_json)

    return result_json

def test_scrape_http_data_retries():
    with_retry = 0
    without_retry = 0
    for x in range(20):
        try:
            result_dict = test_scrape_http_data()
        except:
            logging.error(f"URL was not successfully fetched, NO RETRY")
        if type(result_dict) != dict:
            without_retry += 1
        sleep(0.5 + random())
    for x in range(20):
        for retry in range(1,5):
            try:
                result_dict = test_scrape_http_data()
            except Exception as exc:
                logging.error(f"URL was not successfully fetched, retry number: {retry}")
            else:
                break
        if type(result_dict) != dict:
            with_retry += 1
        sleep(0.5 + random())

    print(f'With retires: {with_retry}')
    print(f'Without retires: {without_retry}')

if __name__ == "__main__":
    yaml_dict = test_load_properties()
    print(yaml_dict)

    # test_render_email()
    # result_dict = test_scrape_http_data()
    # print(result_dict)

    '''Run multiple times'''
    # result_dict = test_scrape_http_data()
    # data = analyze_data(result_dict, True)
    # print(data)

    '''Render and send email'''
    # src_address = os.getenv('EMAIL_ADDR')
    # src_passwd = os.getenv('EMAIL_PASSWD')
    # dest_address = os.getenv('EMAIL_ADDR2')
    email_subject = "Otomoto notifier - test"
    mail_content = test_render_email()
    send_email(yaml_dict['src_email_addr'], yaml_dict['src_email_passwd'],
               yaml_dict['src_email_smtp_addr'], yaml_dict['src_email_smtp_port'],
               yaml_dict['dest_email'][0], email_subject, mail_content)

    #test_scrape_http_data_retries()
    print('end')
