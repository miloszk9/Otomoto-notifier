import os
import logging
import functions

def main():
    # email_address = os.getenv('EMAIL_ADDR')
    # email_passwd = os.getenv('EMAIL_PASSWD')

    # if not email_address or not email_passwd:
    #     logging.ERROR("Email address or password not set")
    #     return False

    url_path = os.getenv('URL_FILE', './urls.yml')
    urls = functions.load_urls(url_path)
    if not urls:
        return False

    for url in urls:
        functions.http_parser(url)
    
    return True

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    if main():
        logging.info("Script execution finished successfully")
    else:
        logging.error("Script execution failed")
