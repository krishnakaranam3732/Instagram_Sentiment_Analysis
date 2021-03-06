import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from os import devnull
import time


class Account:
    def __init__(self, username):
        self.instagram = "https://www.instagram.com"
        self.link = self.instagram + "/" + username
        self.page = None

    def load_full_page(self):
        print("Using Selenium to load full page")
        # # temperorily using this to populate self.page
        # with open("page_source.txt",
        #           encoding='utf-8',
        #           errors='ignore') as file:
        #     self.page = file.read()
        # self.page = requests.get(self.link)
        # print(self.page.content)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(
                 # executable_path='/usr/bin/chromedriver',
                 options=options, service_log_path=devnull)
        driver.get(self.link)
        driver.maximize_window()
        time.sleep(2)
        posts = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/a/span'
        picture = '//*[@id="react-root"]/section/main/div/header/div/div/span/img'
        num_posts = driver.find_element_by_xpath(posts)
        sleep_secs = 5
        try:
            num_of_posts = num_posts.text.replace(",", "")
            num_of_posts = int(num_of_posts)
            sleep_secs = int(num_of_posts/15)
            print("sleep seconds is " + str(sleep_secs))
        except Exception as e:
            print("Exception occured: ", str(e))

        t_end = time.time() + sleep_secs

        script = "window.scrollTo(0, 50000);"

        while time.time() < t_end:
            print("I'm executing")
            # element = driver.find_element_by_xpath(picture)
            # element.send_keys(Keys.END)
            # driver.find_element_by_tag_name("body").send_keys(Keys.END)
            # driver.execute_script(script)
            # driver.find_element_by_tag_name('article').send_keys(Keys.END)
            links = driver.find_elements_by_tag_name('a')
            print(str(len(links)) + " " + links[-1].text)
            driver.execute_script('arguments[0].scrollIntoView(false);',
                                  links[-1])
            time.sleep(2)
            # time.sleep(2)


        # end = "//*[@id="react-root"]/section/footer/div/span"
        # get_end = more = driver.find_element_by_xpath(end)

        # lenOfPage = driver.execute_script(script)
        # match = False
        # while not match:
        #     print("Scrolling")
        #     lastCount = lenOfPage
        #     lenOfPage = driver.execute_script(script)
        #     time.sleep(2)
        #     if lastCount == lenOfPage:
        #         match = True

        self.page = driver.page_source
        driver.close()

    def get_posts(self):
        soup = BeautifulSoup(self.page, 'html.parser')
        soup = soup.find("article")

        posts_li = soup.find_all("a")
        posts = []

        for each_li in posts_li:
            post_link = each_li['href']
            if post_link:
                posts.append(self.instagram + post_link)
        self.page = None
        return posts

    # def clean_comment(self, comment):
    #     final_comment = ""
    #     skip = False
    #     for ch in comment.lower():
    #         if ch == ' ':
    #             skip = False
    #             final_comment += ch
    #         elif ch == '@':
    #             skip = True
    #         elif not skip:
    #             if ch == '.':
    #                 final_comment += " "
    #             elif ch.isalpha() or ch.isdigit() or ch == "’" or ch == "'":
    #                 final_comment += ch
    #     return final_comment

    # def get_comment_text(self, comments):
    #     return " ".join(comments)

    # def get_sentiment(self, comment_text):
    #     analysis = TextBlob(comment_text)
    #     if analysis.sentiment.polarity > 0:
    #         return 'positive'
    #     elif analysis.sentiment.polarity == 0:
    #         return 'neutral'
    #     else:
    #         return 'negative'
