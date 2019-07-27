import random
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from utils import wait, scroll_down

# Logging configuration
logging.basicConfig(level=logging.INFO)

class Bot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        if not os.path.isdir('data/%s' % self.username):
            logging.info('Creating %s data folder' % self.username)
            os.mkdir('data/%s/' % self.username)
        else:
            logging.info('%s data folder already exists' % self.username)
        
        if not os.path.isfile('data/%s/following.txt' % self.username):
            self.following = open('data/%s/following.txt' % self.username, mode='w+')
        else:
            self.following = open('data/%s/following.txt' % self.username, mode='a')

        # Lauching webdriver
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            'cfg/chromedriver', chrome_options=chrome_options)

    def close(self):
        self.driver.close()
        self.following.close()
        print('Closed the bot successfully')

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
        #<p aria-atomic="true" id="slfErrorAlert" role="alert">Sorry, your password was incorrect. Please double-check your password.</p>
        
        try:
            error_check = self.driver.find_element_by_xpath('//p[@id="slfErrorAlert"]')
            error = error_check.text
            logging.error(error)
            return False
        except:
            logging.info('Login was successfull')
            return True

    def run(self, hashtag, follow=True):
        self.driver.get('https://www.instagram.com/explore/tags/%s/' % hashtag)
        wait(2)

        for i in range(4):
            scroll_down(self.driver)
            wait(2)

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
                user = self.driver.find_element_by_xpath('//link[@rel="canonical"]').get_attribute('href').split('/p')[0]
                self.following.write('%s\n' % user)
                
                try:
                    follow_button = self.driver.find_element_by_xpath(
                    '//button[text()="Follow"]')

                    if follow_button and follow:
                        follow_button.click()

                except Exception as e:
                    logging.info('Already following...')

                
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


if __name__ == "__main__":

    hashtags = ['maquiagembatatais', 'makeupbatatais', 'makeupbrasil', 'batataismake', 'beatrizbuenomakeup' 'makebatatais']
    rougeBot = Bot('btsrouge', 'jc21096700')
    if rougeBot.login():
        for hashtag in hashtags:
            rougeBot.run(hashtag, follow=True)

        logging.info('Bot ran smooth')
        rougeBot.close()
    else:
        rougeBot.close()
    
    