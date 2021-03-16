from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    #Set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #1. NASA NEWS
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find title of most recent article
    news_title = soup.find_all('li', class_='slide')[0].find('div', class_='content_title').a.text

    #Find the paragraph of the most recent article
    news_p = soup.find_all('li', class_='slide')[0].find('div', class_='article_teaser_body').text

    #2. MARS SPACE IMAGES
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #Visit URL and generate HTML object
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Navigate to image of the first featured card and regenerate HTML object
    browser.visit('https://www.jpl.nasa.gov'+ soup.find('div', class_='SearchResultCard').a['href'])
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Store url of high-res image
    featured_image_url = soup.find('img', class_='BaseImage')['src']

    #3. MARS FACTS
    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    #Get all tables with Pandas
    tables = pd.read_html(url)

    #Format Table
    df = tables[0]

    df.rename(columns={0: "", 1: "Mars"}, inplace=True)

    df.set_index("",drop=True, inplace=True)

    #Move to HTML string
    mars_facts = df.to_html()

    #4. MARS HEMISPHERES
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    #Visit URL 
    browser.visit(url)

    #Get HTML object and create soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Find descriptions for the 4 products on page
    hemi = soup.find_all('div',class_='description')

    #Retrieve the titles for the 4 products on page
    titles = []

    for x in range(0,len(hemi)):
        titles.append(hemi[x].a.text.split(' E')[0])

    #Retrieve the high res image for the 4 products on page
    urls = []

    for x in range(0,len(hemi)):
        
        #Get path to page containing the high res download
        new_url = 'https://astrogeology.usgs.gov' + hemi[x].a['href']
        
        #Go to download page and update HTML object
        browser.visit(new_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #Find the URL for the high res download
        urls.append(soup.find('div',class_='downloads').a['href'])

    #Build list of dictionary of images
    hemisphere_image_urls = []

    for x in range(0,4):
        hemisphere_image_urls.append({'title':titles[x],'img_url':urls[x]})

    #5. STORE DATA IN DICTIONARY
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'mars_facts': mars_facts,
        'hemisphere_image_url': hemisphere_image_urls
    }

     # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data