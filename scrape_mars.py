
# coding: utf-8

# In[6]:


import requests
from bs4 import BeautifulSoup as soup
import lxml

from splinter import Browser
import pandas as pd


import html5lib
import splinter
import time


# In[10]:


# read the html and get the content and the main title and the paragraph
def get_headline_news():
    page1=requests.get("https://mars.nasa.gov/news/")
    page1_data=soup(page1.content,'lxml')
    headlines_list=page1_data.find('div',class_='content_title')
    headlines_title=headlines_list.a.text.strip()
    headlines_paragraph=page1_data.find('div','rollover_description_inner')
    headlines_para=headlines_paragraph.text.strip()
    return(headlines_title,headlines_para)


# In[15]:


def get_featured_image():
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    image_data = soup(response.text, 'lxml')
    featured_image=image_data.find('ul',class_='articles')
    featured_image =featured_image.find_all('a',class_="fancybox")
    featured_image_url= 'https://www.jpl.nasa.gov' + featured_image[0].get('data-fancybox-href')
    return featured_image_url


# In[31]:


def get_twitter_weather():
    mars_twitter_url='https://twitter.com/marswxreport?lang=en'
    twitter_response=requests.get(mars_twitter_url)
    twitter_data=soup(twitter_response.text,'html.parser')
    twitter_wthr_data = twitter_data.find("div",{"data-name": "Mars Weather"},class_= "tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards has-content",)
    mars_weather = twitter_wthr_data.p.text.strip()
    mars_weather = mars_weather.rstrip("pic.twitter.com/anlHR95BMs")
    return mars_weather


# In[21]:


def get_mars_facts():
    mars_facts_data=pd.read_html('https://space-facts.com/mars/')
    df=mars_facts_data[0]
    df.columns=['Profile Param','Value']
    df.set_index('Profile Param',inplace=True)
    html_table=df.to_html(header = False, border = 0, \
                                                           classes = ['table table-striped table-hover'])
    return html_table

    


# In[32]:





# In[26]:


def get_hemisphere_images():
    executable_path = {'executable_path': 'C:/users/lalit/Beautifulsoup/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html=browser.html
    astro_data = soup(html, 'html.parser')
    image_dict={}
    Image_hemisphere_url=[]
    result_hemis=astro_data.find_all('h3')
    for result in result_hemis:
        image_dict={}
        browser.click_link_by_partial_text(result.text)
        time.sleep(2)
        html=browser.html
        image_data=soup(html,'html.parser')
        image_link=image_data.find_all('div',class_="downloads")
        link=image_link[0].find('a')
        image_url=link.get('href')
        print(image_url)
        print(result.text)
        image_dict["title"]=result.text
        image_dict["image_url"]=image_url
        Image_hemisphere_url.append(image_dict)
        time.sleep(2)
        browser.click_link_by_partial_text('Back')
    browser.quit()
    return Image_hemisphere_url

   


# In[29]:


def scrape():
    Mars_data ={}
    Mars_data["Newsheadlines"],Mars_data["Headline_para"]=get_headline_news()
    Mars_data["featured_image"]=get_featured_image()
    Mars_data["weather"]=get_twitter_weather()
    Mars_data["Mars_facts"]=get_mars_facts()
    Mars_data["Hemisphere_imgs"]=get_hemisphere_images()
    if(not Mars_data['Hemisphere_imgs']):
        Mars_data['Hemisphere_imgs'] = [ { "title" : "Cerberus Hemisphere Enhanced", "image_url" : "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg" }, \
                                        { "title" : "Schiaparelli Hemisphere Enhanced", "image_url" : "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg" }, \
                                        { "title" : "Syrtis Major Hemisphere Enhanced", "image_url" : "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg" }, \
                                        { "title" : "Valles Marineris Hemisphere Enhanced", "image_url" : "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg" } ]
    
    return Mars_data
    


# In[30]:



