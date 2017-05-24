import requests
import logging
import time

from random import randint

resend = 'Resend your activation email'
already_done = 'account has already been activated'
success = 'Thank you for signing up! Your account is now active'
sleep_min = 15
sleep_max = 30

user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36")


logging.basicConfig(format='%(asctime)s[%(levelname)s] %(message)s', datefmt='[%d/%m/%Y][%I:%M:%S %p]', level=logging.INFO)

def parse_file():
    with open('link.txt') as f:
        contents = f.readlines()
    contents = [x.strip() for x in contents]
    return contents

def main():
    contents = parse_file()
    logging.info('Started processing url.')

    count = len(contents)
    logging.info('Total of {} url to verify.'.format(count))
    
    for url in contents:
        logging.info('Processing next url. Items left in queue: {}'.format(count))
        response = requests.get(url, headers={'user-agent': user_agent})
        if response.status_code == 200:
            if resend in response.content:
                logging.info('Expired verification link: {}.'.format(url))
            elif already_done in response.content:
                logging.info('Account was already activated: {}.'.format(url))
            elif success in response.content:
                logging.info('Account activated: {}.'.format(url))
        elif response.status_code == 503:
            logging.info('PTC rate limit triggered, received a 503 response.')
            quit()
        else:
            logging.info('Request failed with status code: {}'.format(response.status_code))
            
        count = count - 1
        time.sleep(randint(sleep_min, sleep_max))
            
    logging.info('Finished processing all url.')
    


if __name__ == '__main__':
    main()
