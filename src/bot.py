import random
import os
import logging
import pymongo
import re
from tqdm import tqdm
from itertools import combinations
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

    def __init__(self, username, password, blacklist=[]):
        self.blacklist = blacklist
        self.username = username
        self.password = password
        # Lauching webdriver

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
        chrome_options.add_experimental_option(
            "prefs", {"profile.block_third_party_cookies": True})

        self.driver = webdriver.Chrome(
            'config/chromedriver', chrome_options=chrome_options)

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
            '//button[contains(text(),"Log In")]')
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
        for letter in self.username:
            username_input.send_keys(letter)
            wait(random.randint(1, 7)/30)
        for letter in self.password:
            password_input.send_keys(letter)
            wait(random.randint(1, 7)/30)

        # username_input.send_keys(self.username)
        # password_input.send_keys(self.password)
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

    def get_friends(self):
        self.driver.get('https://www.instagram.com/%s/' % self.username)
        wait(3)
        follower_button = self.driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a')

        follower_button.click()
        wait(3)

        sugs = None

        try:
            sugs = self.driver.find_element_by_xpath(
                '//h4[contains(text(), Suggestions)]')
        except:
            pass
        scroll_box = self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1

        while last_ht != ht:
            last_ht = ht
            # N tem muito seguidor
            if ht == 1 and sugs:
                print('poucos seguidoress seguindo')
                wait(1)
                break
            else:
                wait(0.5)
                ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)

        #links = scroll_box.find_elements_by_tag_name("a")

        links = (scroll_box.find_elements_by_xpath(
            '//div[@class="PZuss"]//a[text()!=""]'))
        # print(links)
        names = ['@%s' % name.text for name in links if name.text != '']

        print('Vc tem %d seguidores/seguindo' % len(names))

        return names

    def run(self, promo_link, n_comb=1, follow=True):
        #self.friends = ['@lucaporto', '@leu.py', '@antonioomoreira', '@vitubrisola']
        # ['@lucaporto', '@leu.py', '@antonioomoreira', '@vitubrisola']
        self.friends = self.get_friends()

        for b in self.blacklist:
            if b in self.blacklist:
                self.friends.remove(b)

        self.driver.get(promo_link)
        wait(3)


        combs = list(combinations(self.friends, n_comb))
        random.shuffle(combs)
        random.shuffle(combs)


        combs = random.sample(combs, k=round(len(combs)*0.35))

        print('Numero de entradas na promoção %d' % len(combs))

        i = 1
        for combination in tqdm(combs):
            wait(1)
            for _ in range(1):
                scroll_down(self.driver)
                wait(0.4)

            wait(random.uniform(0.4, 0.5))
            comment_section = self.driver.find_element_by_xpath(
                '//textarea[@class="Ypffh"]')
            wait(0.2)
            comment_section.click()
            wait(random.uniform(0.2, 0.6))
            comment_section = self.driver.find_element_by_xpath(
                '//textarea[@class="Ypffh focus-visible"]')
            comment_section.click()
            wait(0.4)
            comment_section.clear()
            
            
            # Inputing info

            fake_string_n = random.randint(1, 20)
            fake_string = 'olha o pc '

            if fake_string_n > 17:
                fake_string = 'nossa o pc é mto bom '
            elif fake_string_n > 14:
                fake_string = 'vamo ganhar '
            elif fake_string_n > 9:
                fake_string = 'olha esse pc so uns 15k '
            elif fake_string_n > 5:
                fake_string = 'viu ?'
            elif fake_string_n > 3:
                fake_string = 'putz olha '

            for letter in fake_string:
                comment_section.send_keys(letter)
                wait(random.randint(1, 4)/30)

            for friend in combination:

                for letter in friend:
                    comment_section.send_keys(letter)
                    wait(random.randint(1, 7)/30)
                
                comment_section.send_keys(' ')

            wait(0.5)
            post_button = comment_section = self.driver.find_element_by_xpath(
                '//button[contains(text(),"Post")]')
            wait(0.2)
            post_button.submit()
            wait(random.uniform(1.4, 2.3))
            i += 1

            if i % 8 == 0:
                self.driver.get(promo_link)
                wait(1)

            if i % 100 == 0:
                wait(600)

            wait(1)

    def like_and_follow(self, hashtag, follow=True):
        self.driver.get('https://www.instagram.com/explore/tags/%s/' % hashtag)
        wait(2)

        for _ in range(9):
            scroll_down(self.driver)
            wait(0.5)

        # Using set to make unique hrefs
        hrefs = set([item.get_attribute('href') for item in self.driver.find_elements_by_tag_name(
            'a') if '.com/p/' in item.get_attribute('href')])

        logging.info('Unique photos %d' % len(hrefs))

        i = 1
        unique_photos = len(hrefs)
        for pic_href in hrefs:
            self.driver.get(pic_href)
            wait(1)
            scroll_down(self.driver)

            try:
                wait(random.uniform(1, 2.3))

                try:
                    # Following section
                    follow_button = self.driver.find_element_by_xpath(
                        '//button[text()="Follow"]')

                    if follow_button and follow:
                        follow_button.click()

                except Exception as e:
                    logging.info('Already following...')

                # Liking section
                like_button = self.driver.find_element_by_xpath(
                    '//button[@class="wpO6b "]')
                like_button.click()
                # Seguir as pessos

                likes_ = self.driver.find_element_by_xpath(
                    '//a[@class="zV_Nj"]')

                if likes_:
                    likes_.click()
                    wait(0.4)

                    scroll_box = self.driver.find_element_by_xpath(
                        '//div[@class="                   Igw0E     IwRSH      eGOV_        vwCYk                                                                            i0EQd                                   "]')
                    
                    last_ht, ht = 0, 1
                    
                    while last_ht != ht:
                        last_ht = ht
                        ht = self.driver.execute_script("""
                        arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                        return arguments[0].scrollHeight;
                        """, scroll_box)

                        f_buttons = scroll_box.find_elements_by_xpath('//button[@class="sqdOP  L3NKy   y3zKF     "]')#'//button[text()="Follow"]')

                        print('N follows no scroll %d' % len(f_buttons))

                        for f_button in f_buttons:
                            f_button.click()
                            wait(random.uniform(0.9, 1.8))
                        wait(1)
                        
                sleeptime = random.randint(14, 17)

                if i % 4 == 0:
                    self.driver.get(
                'https://www.google.com.br/')
                    sleeptime = 30
                for second in reversed(range(0, sleeptime)):
                    logging.info("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                 + " | Sleeping " + str(second))
                    wait(random.uniform(0.5, 1))

            except Exception as e:
                logging.error(e)
                wait(2)
            i += 1
            unique_photos -= 1

    def follow(self, hashtag, follow=True):
        self.driver.get('https://www.instagram.com/explore/tags/%s/' % hashtag)
        wait(2)

        # Using set to make unique hrefs
        hrefs = set([item.get_attribute('href') for item in self.driver.find_elements_by_tag_name(
            'a') if '.com/p/' in item.get_attribute('href')])

        hrefs = list(hrefs)[:4]

        logging.info('N photos %d' % len(hrefs))

        unique_photos = len(hrefs)
        for pic_href in hrefs:
            self.driver.get(pic_href)
            try:
                wait(random.uniform(1, 2.3))

                try:
                    # Following section
                    follow_button = self.driver.find_element_by_xpath(
                        '//button[text()="Follow"]')

                    if follow_button and follow:

                        follow_button.click()

                except Exception as e:
                    logging.info('Already following...')

                # Liking section
                like_button = self.driver.find_element_by_xpath(
                    '//button[@class="wpO6b "]')
                like_button.click()

                for second in reversed(range(0, random.randint(4, 9))):
                    logging.info("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                 + " | Sleeping " + str(second))
                    wait(random.uniform(0.5, 1))

            except Exception as e:
                logging.error(e)
                wait(2)

            unique_photos -= 1
