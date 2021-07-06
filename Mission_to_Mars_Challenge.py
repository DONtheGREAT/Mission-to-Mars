#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page,
# we're searching for elements with a specific combination of tag (div) and attribute (list_text)
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
# CSS works from right to left, such as returning the last item on the list instead of the first
# Because of this, when using select_one, the first matching element returned will be a <li />
# element with a class of slide and all nested elements within it
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem


# In[6]:


slide_elem.find('div', class_='content_title')


# In[7]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# .get_text(). When this new method is chained onto .find(), only the text of the element is returned.
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[8]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[9]:


## change code type to markdown before typing next section,
# running will execute words as markdown then change back to code.


# ### JPL Space Images Featured Image

# In[10]:


# Visit URL containing image.
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[11]:


# Find and click the full image button
# List 1 because we want to click the 2nd appearance of the button tag,
# and there are 3.
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# html for the PAGE of the full size image
img_soup


# In[14]:


# Find the relative image url,
# find the unique class and key of the image instead of the value,
# or you will pull the same image everytime instead of the most recent image.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
# get src grabs the link to the image in this specific tag.
img_url_rel


# In[15]:


# Use the base URL to create an absolute URL
# add the base url because the image url will not work by itself.
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[16]:


# The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML.
# By specifying an index of 0, we're telling Pandas to pull only the first table it encounters
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# assign columns
df.columns=['description', 'Mars', 'Earth']
# make the description the dataframes index, inplace is it makes changes to initial variable, no need to create another one.
df.set_index('description', inplace=True)
df


# In[17]:


# convert our DataFrame back into HTML-ready code using the .to_html() function to add it to a webpage
df.to_html()


# In[18]:


# download code as python file for automating the code


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[20]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[21]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for x in range (4):
    hemispheres = {}
    
    #Parse the resulting html with soup
    html = browser.html
    hem_soup = soup(html, 'html.parser')
    
    # Find & Click Hemisphere Link
    hem_link = browser.find_by_tag('h3')[x]
    hem_link.click()    
     
    # Parse the resulting html with soup (initially had this before the find & click but was experiencing and No object error so added 2 instances)
    html = browser.html
    hem_soup = soup(html, 'html.parser')
    
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    
    # Retrieve the title
    hem_title = hem_soup.find('h2').get_text() 
        
    # Find the relative image url
        
    hemi_img_url_rel = hem_soup.find('img', class_='wide-image').get('src') 
    
    # Use the base url to create an absolute url
    img_url = f'https://marshemispheres.com/{hemi_img_url_rel}'
    
    #storing results in the dictionary
    hemispheres = {
        'FullRes_image_url': img_url,
        'Title': hem_title
        
    }
    
    #appending to dict
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# In[22]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[ ]:


# 5. Quit the browser
browser.quit()

