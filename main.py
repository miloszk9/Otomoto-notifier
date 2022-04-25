import os
import logging
import functions

def main():
    email_src_address = os.getenv('EMAIL_ADDR')
    email_src_passwd = os.getenv('EMAIL_PASSWD')

    if not email_src_address or not email_src_passwd:
        logging.error("Email address or password not set")
        return False

    yaml_path = os.getenv('URL_FILE', './config.yml')
    yaml_dict = functions.load_properties(yaml_path)

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
    processed_dict = functions.analyze_data(cars_dict, is_hourly)

    if type(processed_dict) is not dict:
        logging.error("Failed to analyze data")
        return False

    if is_hourly and len(processed_dict["new"]) == 0 and len(processed_dict["gone"]) == 0:
        logging.info("No updates to be send.")
        return True
        
    html_template = functions.render_email(processed_dict)
    if not html_template:
        logging.error("Failed to render email")
        return False
    
    for dest_email in yaml_dict['dest_email']:
        send_status = functions.send_email(email_src_address, email_src_passwd, dest_email, is_hourly, html_template)
    
        if not send_status:
            logging.error("Failed to send email")
            return False

    return True

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if main():
        logging.info("Script execution finished successfully")
    else:
        logging.error("Script execution failed")
