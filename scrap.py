from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

import time
import re


#browser =  webdriver.Chrome(executable_path=r"C:\Users\pablo\Downloads\chromedriver.exe")


def recent_25_posts(username):
    """With the input of an account page, scrape the 25 most recent posts urls"""
    url = "https://www.instagram.com/" + username + "/"
    browser =  webdriver.Chrome(executable_path=r"C:\Users\pablo\Downloads\chromedriver.exe")

    #browser = Chrome()
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < 5:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(5)
    else:
        return post_links[:5]



def insta_details(urls):


    """Take a post url and return post details"""
    #browser = Chrome()
    browser =  webdriver.Chrome(executable_path=r"C:\Users\pablo\Downloads\chromedriver.exe")

    post_details = []
    for link in urls:
        browser.get(link)
        try:
        # This captures the standard like count. 
            likes = browser.find_element_by_partial_link_text('gusta').text
        except:
        # This captures the like count for videos which is stored
            xpath_view = '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div'
            likes = browser.find_element_by_xpath(xpath_view).text
        age = browser.find_element_by_css_selector('a time').text
        xpath_comment = '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[1]/ul'
        comment = browser.find_element_by_xpath(xpath_comment).text
        insta_link = link.replace('https://www.instagram.com/p','')
        post_details.append({'link': insta_link,'likes/views': likes,'age': age, 'comment': comment})
        time.sleep(10)
    return post_details

def find_hashtags(comment):
	hashtags = re.findall('#[A-Za-z]+', comment)
	return hashtags


def clean_likes(t):
	x = re.split("\s", t, 1)
	n_likes = int(x[0])
	return n_likes



pablin_urls=recent_25_posts('pablintango')

pablin_details=insta_details(pablin_urls)

#print(pablin_urls)
#print(pablin_details)

############################################################
# por que no funca esto?

pablin=pd.DataFrame(pablin_details)
pablin['hashtags']=pablin['comment'].apply(lambda x: find_hashtags(x))
pablin['likes/views']=pablin['likes/views'].apply(lambda x: clean_likes(x))


ax = pablin.plot.bar(x='age',y='likes/views', rot=0)

# pablin.plot(y='likes/views', x='age',color='orange')
# plt.xticks(rotation=60)
plt.show()

pablin.to_csv('informe_pablintango.csv')
