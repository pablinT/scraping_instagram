
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import re




def recent_25_posts(username):
    """With the input of an account page, scrape the 25 most recent posts urls"""
    url = "https://www.instagram.com/" + username + "/"
    browser =  webdriver.Chrome(executable_path=r"C:\Users\pablo\Downloads\chromedriver.exe")

    #browser = Chrome()
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < 25:
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(5)
    else:
        return post_links[:25]



def insta_details(urls):

    """para cada url extraemos los detalles"""
    #la ubicacion del chromedriver.exe
    #browser = Chrome()
    browser =  webdriver.Chrome(executable_path=r"C:\Users\pablo\Downloads\chromedriver.exe")

    post_details = []
    for link in urls:
        browser.get(link)
        try:
        # extraemos los likes, si tu navegador está en otro idioma hay que cambiar el 'gusta' 
            likes = browser.find_element_by_partial_link_text('gusta').text
        except:
        # extraemos los likes de los videos
            xpath_view = '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/section[2]/div'
            likes = browser.find_element_by_xpath(xpath_view).text
	# extraemos la antigüedad del post
        age = browser.find_element_by_css_selector('a time').text
        # ubicamos los comentarios y los extraemos
	xpath_comment = '//*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div[1]/ul'
        comment = browser.find_element_by_xpath(xpath_comment).text
        insta_link = link.replace('https://www.instagram.com/p','')
        post_details.append({'link': insta_link,'likes/views': likes,'age': age, 'comment': comment})
        time.sleep(10)
    return post_details

#definimos la funcion que extrae los hashtags
def find_hashtags(comment):
	hashtags = re.findall('#[A-Za-z]+', comment)
	return hashtags

#definimos la funcion que limpia la columna de likes y los convierte en enteros
def clean_likes(t):
	x = re.split("\s", t, 1)
	n_likes = int(x[0])
	return n_likes

#obtengo las url de los ultimos 25 posteos
pablin_urls=recent_25_posts('pablintango')

#evaluo la funcion en cada una de las 25 urls
pablin_details=insta_details(pablin_urls)

#construyo el dataframe
pablin=pd.DataFrame(pablin_details)

#creo la columna hashtags, extraigo los hashtags y convierto los likes en enteros
pablin['hashtags']=pablin['comment'].apply(lambda x: find_hashtags(x))
pablin['likes/views']=pablin['likes/views'].apply(lambda x: clean_likes(x))

#ploteo los datos
ax = pablin.plot.bar(x='age',y='likes/views', rot=0)
plt.show()

#exporto a un csv
pablin.to_csv('informe_pablintango.csv')
