from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import requests

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

# Latest News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    title = soup.find_all(class_='content_title')
    latest_title = title[1].a.text
    latest_para = soup.find(class_='article_teaser_body').text
# Full Image
    url_mars = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_mars)
    browser.find_by_id('full_image').click()
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")  
    relative_image_path = soup.find_all('img')[3]['src']
    base_url = 'https://www.jpl.nasa.gov'
    full_image_url = base_url + relative_image_path
# Table
    url_table = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_table)
    mars_facts = tables[0]
    html_table = mars_facts.to_html()
    html_table.replace('\n', '')    
    mars_facts.to_html('table.html')
# Hemispheres
    astr_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astr_url)
    html = browser.html
    soup = bs(html, "html.parser")
    x = soup.find_all('h3')
    y = soup.find_all(class_='description')
    mars_url_base = 'https://astrogeology.usgs.gov'
    hemisphere_list = []

    for i in range(0, 4):
        title = x[i].text
        img_url = mars_url_base + y[i].a['href']
        browser.visit(img_url)
        html = browser.html
        soup = bs(html, "html.parser") 
        image_path = soup.find('li').a['href']
        browser.visit(astr_url)
        html = browser.html
        soup = bs(html, "html.parser")
        
        hemisphere = {
                'title': title,
                'img_url': image_path,
            }
        hemisphere_list.append(hemisphere)

    mars_data = {
        "Latest_News_Title":latest_title,
        "Latest_News_Preview":latest_para,
        "Full_Image": full_image_url,
        "Hemisphere_1_title": hemisphere_list[0]['title'],
        "Hemisphere_2_title": hemisphere_list[1]['title'],
        "Hemisphere_3_title": hemisphere_list[2]['title'],
        "Hemisphere_4_title": hemisphere_list[3]['title'],
        "Hemisphere_1_url": hemisphere_list[0]['img_url'],
        "Hemisphere_2_url": hemisphere_list[1]['img_url'],
        "Hemisphere_3_url": hemisphere_list[2]['img_url'],
        "Hemisphere_4_url": hemisphere_list[3]['img_url']
    }

    browser.quit()

    # Return results
    return mars_data
scrape_info()

