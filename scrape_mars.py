
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time






def scrape():
    mars = {}

    #nasa mars_news
    url_news = 'https://mars.nasa.gov/news/'
    response_news = requests.get(url_news)
    soup_news = BeautifulSoup(response_news.text,'html.parser')

    #find the title a tag to which the title is located in This will find the most recent tag
    title_object=soup_news.find('div',class_='content_title')
    news_title=title_object.a.text.strip()
    mars['title'] = news_title

    #access the first paragraph from the first article by taking the link and combine it with the original url link
    #to the home page
    url_news_article = 'https://mars.nasa.gov'
    url_paragraph= url_news_article + title_object.a['href']
    response_new_paragraph = requests.get(url_paragraph)
    soup_paragraph = BeautifulSoup(response_new_paragraph.text,'html.parser')

    #get the first paragraph from the first article 
    paragraph_scraped=soup_paragraph.find('div', {"class": "clearfix"})
    news_p = paragraph_scraped.p.text
    mars['news_paragraph']= news_p

    #jpl space images
    browser_jpl = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser_jpl.visit(url)
    browser_jpl.click_link_by_partial_text('FULL IMAGE')

    # convert the htlm document to a txt file 
    html = browser_jpl.html
    soup_jpl = BeautifulSoup(html, 'html.parser')

    # find the image and retreive the partial url
    img_jp=soup_jpl.find('img', class_='fancybox-image')


    browser_jpl = Browser('chrome', headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser_jpl.visit(url)
    full_image_element = browser_jpl.click_link_by_partial_text('FULL IMAGE')

    time.sleep(1)
    more_info_element = browser_jpl.find_link_by_partial_text('more info')
    more_info_element.click()

    more_info_html = browser_jpl.html

    featured_html_soup = BeautifulSoup(more_info_html,'html.parser')

    img_tag=featured_html_soup.find('figure', class_='lede').find('img')['src']
    img_url_concat = "https://www.jpl.nasa.gov"+img_tag
    mars["featured_img"]= img_url_concat

    #mars_weather
    url_weather = 'https://twitter.com/marswxreport?lang=e'
    response_weather = requests.get(url_weather)

    soup_weather = BeautifulSoup(response_weather.text,'html.parser')
    weather_results = soup_weather.find_all('div', class_='js-tweet-text-container')

    #append the results to the mars dictionary
    mars_weather = weather_results[0].p.text
    mars['weather']= mars_weather


    #make a pandas table form the html and then send it back to a table
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)

    #set the table to be html
    table = df.to_html()
    table = table.replace('\n', '')
    
    #add to the mars dictonary as a new key value pair
    mars['fact'] = table
    
    return mars





