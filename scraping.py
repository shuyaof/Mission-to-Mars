# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt

data = {}

def scrape_all():

    # Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }
    # 5. Quit the browser
    browser.quit()
    return data
    
def mars_news(browser):   
    ### Visit the NASA Mars News Site
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')
    slide_elem.find('div', class_='content_title')
    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
   
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    return news_title,news_p

def featured_image(browser):
    ### JPL Space Images Featured Image
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()
    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    # find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

def mars_facts():    
### Mars Facts
    df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    return df.to_html(classes="table table-striped")

# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
### Hemispheres
# Set the executable path and initialize Splinter

def hemispheres(browser):
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #   Retrieve all images that contain mars hemisphere information
    items = img_soup.find_all('div', class_='item')
    hemispheres_main_url='https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/'
    # 4. Print the list that holds the dictionary of each image url and title.
    # Create empty list for hemisphere urls
    hemisphere_image_urls = []
    for i in items:
        #store titles
        title=i.find('h3').text
        partial_img_url = i.find('a',class_='itemLink product-item')['href']
        #store full link that leads to full image
        img_url=hemispheres_main_url + partial_img_url
        browser.visit(img_url)
        partial_img_html=browser.html
        partial_soup=soup(partial_img_html,'html.parser')
        img_url=hemispheres_main_url + partial_soup.find('img',class_='wide-image')['src']
        hemisphere_image_urls.append({"title":title, "img_url":img_url})
    return hemisphere_image_urls
        
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


