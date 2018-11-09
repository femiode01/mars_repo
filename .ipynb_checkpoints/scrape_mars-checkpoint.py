from splinter import Browser
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd

# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/Lexus/Desktop/chrome/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# Function to scrape for weather in Cost Rica
def scrape_mars():

    data = {}
    data["news_title"] = nasa_mars()
    data["news_p"] =  nasa_mars()
    data["feature_img"] = space_images()
    data["mars_weather"] = mars_weather()
    data["html_table"] = mars_facts()
    data["mars_hemisphere"] = mars_hemisphere()

    return data



def nasa_mars():

    # Initialize browser
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text
    
    return news_title
    return news_p

def space_images():

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find('a', class_= 'button fancybox')['data-fancybox-href']
    feature_img = 'https://www.jpl.nasa.gov' + image

    return feature_img

def mars_weather():
    
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_weather = soup.find_all('p')[5].get_text()
    
    return mars_weather


def mars_facts():
    
    import pandas as pd
    url = 'http://space-facts.com/mars/'
    browser.visit(url)
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Category', 'Value']
    html_table = df.to_html()
    html_table.replace('\n', '')
    
    return html_table

def mars_hemispheres():
    
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []
    products = soup.find("div", class_ = "collapsible results" )
    hemispheres = products.find_all("div", class_="item")

    for hemis in hemispheres:
        title = hemis.find("h3").text
        title = title.replace("Enhanced", "")
        link = hemis.find("a")["href"]
        img_link = "https://astrogeology.usgs.gov/" + link    
        browser.visit(img_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    
    
    return mars_hemisphere
    
    
    

