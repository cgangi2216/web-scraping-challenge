# Dependancies
import pandas as pd
import pprint as pp
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrap_data():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Create empty dictionary for output data
    output_data = {}

    # ======================== NASA Mars News ========================
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.select_one('div.list_text')
    output_data['article_title'] = element.find('div',class_='content_title').get_text()
    output_data['article_summary'] = element.find('div',class_='article_teaser_body').get_text()


    # ======================== JPL Mars Space Images - Featured Image ========================
    img_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(img_url)
    img_button = browser.find_by_css('button.btn.btn-outline-light')
    img_button.click()
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')
    full_img_url = img_soup.find('img', class_='fancybox-image').get('src')
    output_data['featured_image_url'] = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{full_img_url}'


    # ======================== Mars Facts ========================
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    mars_facts = pd.read_html(facts_url)[0]
    mars_facts = mars_facts.rename(columns={0:'Measure',1:'Value'})
    mars_facts.set_index('Measure')
    mars_facts = mars_facts.to_html()
    output_data['mars_facts'] = mars_facts


    # ======================== Mars Hemispheres ========================
    base_url = 'https://astrogeology.usgs.gov'
    mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_url)
    html = browser.html
    mars_soup = BeautifulSoup(html, 'html.parser')

    # List all hemisphere items
    itemLink_ls = mars_soup.find_all('div',class_='description')

    # Create placeholder variables
    hemisphere_image_urls = []
    itemLink_url = ''
    title = ''
    full_img_url = ''

    # Loop through hemisphere items
    for item in itemLink_ls:
        if (item.a):
            itemLink_url = item.a.get('href')
            itemLink_url = f'{base_url}{itemLink_url}'
            if (item.a.h3):
                title = item.a.h3.get_text()
        
        # Get full image url
        browser.visit(itemLink_url)
        html = browser.html
        hem_soup = BeautifulSoup(html, 'html.parser')
        
        x = hem_soup.find('div', class_='downloads')
        if (x.ul):
            if (x.li):
                if (x.a):
                    full_img_url = x.ul.li.a.get('href')
        
        # Apend to list
        hemisphere_image_urls.append({'hemisphere_name':title, 'hemisphere_image_url':full_img_url})

        # Reset variables
        itemLink_url = ''
        title = ''
        full_img_url = ''   
    
    output_data['hemispheres'] = hemisphere_image_urls

    # ======================== Close browser & return scrapped data ========================
    browser.quit()

    return output_data


scrap_data()