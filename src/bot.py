import random
import os
import logging
import pymongo
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from utils import wait, scroll_down
from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / 'cfg/.env'
load_dotenv(dotenv_path=env_path)

# Logging configuration
logging.basicConfig(level=logging.INFO)
follower_regex = re.compile(r'\(@(.*)\)', re.U | re.I)


class Bot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db_client = pymongo.MongoClient("mongodb+srv://%s:%s@cluster-ogeng.mongodb.net/test?retryWrites=true&w=majority" %
                                             (os.getenv('MONGO_USER'), os.getenv('MONGO_PASSWORD')))

        self.db = self.db_client.get_database('db')
        self.following = self.db.following
        # Lauching webdriver

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            'cfg/chromedriver', chrome_options=chrome_options)

    def close(self):
        self.driver.close()
        logging.info('Closed the bot successfully')

    def login(self):
        # <a href='/accounts/login/?source=auth_switcher'>Conecte-se</a> //a[@href'accounts/login']
        # <input> //input[@name='username']
        # <input> //input[@name='password']
        # loading main insta page
        self.driver.get('https://www.instagram.com/')
        wait(2)
        # Finding login button and clicking it
        login_button = self.driver.find_element_by_xpath(
            '//a[contains(@href,"accounts/login")]')
        login_button.click()
        wait(2)
        # Login in the user
        username_input = self.driver.find_element_by_xpath(
            '//input[@name="username"]')
        password_input = self.driver.find_element_by_xpath(
            '//input[@name="password"]')
        # cleaning trash data
        username_input.clear()
        password_input.clear()
        # Inputing info
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        # Pressing enter and login
        password_input.send_keys(Keys.RETURN)
        wait(3)
        # <p aria-atomic="true" id="slfErrorAlert" role="alert">Sorry, your password was incorrect. Please double-check your password.</p>

        try:
            error_check = self.driver.find_element_by_xpath(
                '//p[@id="slfErrorAlert"]')
            error = error_check.text
            logging.error(error)
            return False
        except:
            logging.info('Login was successfull')
            return True

    def run(self, hashtag, follow=True):
        self.driver.get('https://www.instagram.com/explore/tags/%s/' % hashtag)
        wait(2)

        for _ in range(4):
            scroll_down(self.driver)
            wait(1)

        # Using set to make unique hrefs
        hrefs = set([item.get_attribute('href') for item in self.driver.find_elements_by_tag_name(
            'a') if '.com/p/' in item.get_attribute('href')])

        logging.info('Unique photos %d' % len(hrefs))

        unique_photos = len(hrefs)
        for pic_href in hrefs:
            self.driver.get(pic_href)
            wait(2)
            scroll_down(self.driver)

            try:
                wait(random.randint(2, 4))

                try:
                    # Following section
                    follow_button = self.driver.find_element_by_xpath(
                        '//button[text()="Follow"]')

                    if follow_button and follow:
                        meta_content = self.driver.find_element_by_xpath(
                            '//meta[@property="og:description"]').get_attribute('content')
                        user = follower_regex.search(meta_content).group(1)

                        self.following.update(
                            {'user': user}, {'user': user, 'follower': self.username}, upsert=True)

                        follow_button.click()

                except Exception as e:
                    logging.info('Already following...')

                # Liking section
                like_button = self.driver.find_element_by_xpath(
                    '//span[@aria-label="Like"]')
                like_button.click()

                for second in reversed(range(0, random.randint(18, 28))):
                    logging.info("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                 + " | Sleeping " + str(second))
                    wait(1)

            except Exception as e:
                logging.error(e)
                wait(2)

            unique_photos -= 1
