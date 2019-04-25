import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from os import devnull
import time


class Account:
    def __init__(self, username):
        self.instagram = "https://www.instagram.com"
        self.link = self.instagram + "/" + username
        self.page = None

    def load_full_page(self):
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
        # time.sleep(1)
        load_more_comments = "//*[@id='react-root']/section/main/div/" +\
                             "div/article/div[2]/div[1]/ul/li[2]/button"
        more = driver.find_element_by_xpath(load_more_comments)

        while(more):
            print("clicking more")
            actions = ActionChains(driver)
            actions.move_to_element(more).click(more).perform()
            more = driver.find_element_by_xpath(load_more_comments)

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
