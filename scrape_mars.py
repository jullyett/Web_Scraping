from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    
    # NASA Mars News #

    # URL of page to be scraped
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve page with the requests module
    response = requests.get(news_url)

    # Create BeautifulSoup object; 
    time.sleep(5)
    soup_news = BeautifulSoup(response.text, 'html.parser') 

    latest_title = soup_news.find_all(class_='slide')[0]
    latest_title_text = latest_title.find(class_="rollover_description_inner").text.strip()
    latest_title_headline = latest_title.find(class_= "content_title").text.strip()

    # JPL Mars Space Images - Featured Image # 

    browser = init_browser()

    # Visit the following URL
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(10)

    # Design an XPATH selector to grab the current Featured Mars Image
    xpath_1 = '//footer//a[@class="button fancybox"]'
    results_1 = browser.find_by_xpath(xpath_1)
    time.sleep(10)
    img_1 = results_1[0]
    img_1.click()   

    # Use splinter to Click the "more info" Featured Mars Image
    time.sleep(60)
    xpath_2 = '//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]'
    results_2 = browser.find_by_xpath(xpath_2)
    time.sleep(5)
    img_2 = results_2[0]
    img_2.click()

    # Use splinter to Click the current Featured Mars Image
    # to bring up the full resolution image
    time.sleep(10)
    xpath_3 = '//*[@id="page"]/section[1]/div/article/figure/a/img'
    results_3 = browser.find_by_xpath(xpath_3)
    time.sleep(5)
    img_3 = results_3[0]
    img_3.click()

    # Scrape the browser into soup and use soup to find the full resolution image of mars
    # Save the image url to a variable called `img_url`
    html = browser.html
    soup_img = BeautifulSoup(html, 'html.parser')
    time.sleep(5)
    featured_image_url = soup_img.find("img")["src"]

    # Mars Weather #

    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    twitter_response = requests.get(twitter_url)

    # Create BeautifulSoup object
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')

    mars_weather = twitter_soup.find("p", class_='TweetTextSize').text.strip()

    # Mars Facts #

    #Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    facts_url = "https://space-facts.com/mars/"
    facts_table = pd.read_html(facts_url)
    
    output=[]
    for row in facts_table:
        output.append(pd.DataFrame(row))

    facts_pd = pd.concat(output, ignore_index=True)
    facts_pd.columns = ["Description", "Values"]
    facts_pd.set_index("Description", inplace=True)

    #Use Pandas to convert the data to a HTML table string.
    facts_html_table = facts_pd.to_html()
    facts_html_table.replace('\n', '')
    facts_pd.to_html('table.html')

    # Mars Hemispheres #

    browser = init_browser()

    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    root_url = "https://astrogeology.usgs.gov"
    browser.visit(hemispheres_url)

    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    xpath_4pics = '//*[@id="product-section"]/div[2]/div[1]/a/img'
    results_4pics = browser.find_by_xpath(xpath_4pics)
    time.sleep(5)
    all_pics = results_4pics[0]
    all_pics.click()

    #Cerberus
    xpath_cerberus = '//*[@id="wide-image-toggle"]'
    results_cerberus = browser.find_by_xpath(xpath_cerberus)
    time.sleep(5)
    cerberus_img = results_cerberus[0]
    cerberus_img.click()

    # Save the images url to a variable
    html_cerberus = browser.html
    soup_cerberus = BeautifulSoup(html_cerberus, 'html.parser')
    time.sleep(5)
    cerberus_image = soup_cerberus.find("img", class_="wide-image")["src"]
    cerberus_image_url = root_url + cerberus_image
    
    #Click back button
    xpath_back = '//*[@id="splashy"]/div[1]/div[1]/div[3]/section/a'
    results_back = browser.find_by_xpath(xpath_back)
    time.sleep(5)
    back_btn = results_back[0]
    back_btn.click()

    #Schiaparelli
    xpath_schiaparelli = '//*[@id="product-section"]/div[2]/div[2]/div/a/h3'
    results_schiaparelli = browser.find_by_xpath(xpath_schiaparelli)
    time.sleep(5)
    schiaparelli_img = results_schiaparelli[0]
    schiaparelli_img.click()

    # Save the images url to a variable
    html_schiaparelli = browser.html
    soup_schiaparelli = BeautifulSoup(html_schiaparelli, 'html.parser')
    time.sleep(5)
    schiaparelli_image = soup_schiaparelli.find("img", class_="wide-image")["src"]
    schiaparelli_image_url = root_url + schiaparelli_image

    #Click back button
    xpath_back = '//*[@id="splashy"]/div[1]/div[1]/div[3]/section/a'
    results_back = browser.find_by_xpath(xpath_back)
    time.sleep(5)
    back_btn = results_back[0]
    back_btn.click()

    #Syrtis
    xpath_syrtis = '//*[@id="product-section"]/div[2]/div[3]/div/a/h3'
    results_syrtis = browser.find_by_xpath(xpath_syrtis)
    time.sleep(5)
    syrtis_img = results_syrtis[0]
    syrtis_img.click()

    # Save the images url to a variable
    html_syrtis = browser.html
    soup_syrtis = BeautifulSoup(html_syrtis, 'html.parser')
    time.sleep(5)
    syrtis_image = soup_syrtis.find("img", class_="wide-image")["src"]
    syrtis_image_url = root_url + syrtis_image

    #Click back button
    xpath_back = '//*[@id="splashy"]/div[1]/div[1]/div[3]/section/a'
    results_back = browser.find_by_xpath(xpath_back)
    time.sleep(5)
    back_btn = results_back[0]
    back_btn.click()

    #Valles
    xpath_valles = '//*[@id="product-section"]/div[2]/div[4]/div/a/h3'
    results_valles = browser.find_by_xpath(xpath_valles)
    time.sleep(5)
    valles_img = results_valles[0]
    valles_img.click()

    # Save the images url to a variable
    html_valles = browser.html
    soup_valles = BeautifulSoup(html_valles, 'html.parser')
    time.sleep(5)
    valles_image = soup_valles.find("img", class_="wide-image")["src"]
    valles_image_url = root_url + valles_image

    #Save both the image url string for the full resolution hemisphere image and the Hemisphere title containing the hemisphere name. 
    #Use a Python dictionary to store the data using the keys img_url and title.

    dict_Cerberus = {"title": "Cerberus Hemisphere Enhanced", "img_url": cerberus_image_url}
    dict_Schiaparelli = {"title": "Schiaparelli Hemisphere Enhanced", "img_url": schiaparelli_image_url}
    dict_Syrtis = {"title": "Syrtis Major Hemisphere Enhanced", "img_url": syrtis_image_url}
    dict_Valles = {"title": "Valles Marineris Hemisphere Enhanced", "img_url": valles_image_url}

    #Append the dictionary with the image url string and the hemisphere title to a list. 
    #This list will contain one dictionary for each hemisphere.

    Mars_hemispheres = [dict_Cerberus, dict_Schiaparelli, dict_Syrtis, dict_Valles]

    # Store in dictionary

    mars_dict = {
        "latest_headline": latest_title_headline,
        "latest_text": latest_title_text,
        "featured_image": featured_image_url,
        "Mars_weather": mars_weather,
        "Mars_table": facts_pd.to_html(classes=["table", "table-striped", "table-hover", "table-sm"], justify="justify-all"),
        "Hemispheres": Mars_hemispheres,
    }

    browser.quit()
    return mars_dict


