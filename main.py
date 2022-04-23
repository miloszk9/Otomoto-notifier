import os
import logging
import functions

def main():
    email_src_address = os.getenv('EMAIL_ADDR')
    email_src_passwd = os.getenv('EMAIL_PASSWD')

    if not email_src_address or not email_src_passwd:
        logging.ERROR("Email address or password not set")
        return False

    yaml_path = os.getenv('URL_FILE', './config.yml')
    yaml_dict = functions.load_properties(yaml_path)

    for url in yaml_dict['urls']:
        functions.parse_html(url)
    
    # yaml_dict['dest_email']

    return True

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if main():
        logging.info("Script execution finished successfully")
    else:
        logging.error("Script execution failed")
