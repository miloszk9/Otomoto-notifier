import os
import logging
import functions

def main():
    dirname = os.path.dirname(__file__)

    yaml_dict = functions.load_properties(os.path.join(dirname, 'volume/config.yml'))

    if not yaml_dict:
        logging.error("Loading propoerties failed.")
        return False

    cars_dict = dict()

    for url in yaml_dict['urls']:
        for retry in range(1,6):
            try:
                cars_list = functions.scrape_http_data(url)
            except Exception as exc:
                logging.error(f"URL {url} was not successfully fetched, retry number: {retry}")
            else:
                break

        if cars_list:
            cars_dict.update(cars_list)

    is_hourly = os.getenv('IS_HOURLY', False)
    processed_dict = functions.analyze_data(cars_dict, is_hourly, dirname)

    if type(processed_dict) is not dict:
        logging.error("Failed to analyze data")
        return False

    if is_hourly and len(processed_dict["new"]) == 0 and len(processed_dict["gone"]) == 0:
        logging.info("No updates to be send.")
        return True
        
    html_template = functions.render_email(processed_dict, dirname)
    if not html_template:
        logging.error("Failed to render email")
        return False
    
    for dest_email in yaml_dict['dest_email']:
        send_status = functions.send_email(yaml_dict['src_email_addr'], yaml_dict['src_email_passwd'],
                                           dest_email, is_hourly, html_template)
    
        if not send_status:
            logging.error("Failed to send email")
            if is_hourly:
                open(os.path.join(dirname, 'volume/hourly.json'), 'w').close()
            else:
                open(os.path.join(dirname, 'volume/daily.json'), 'w').close()

            return False

    return True

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if main():
        logging.info("Script execution finished successfully")
    else:
        logging.error("Script execution failed")
