from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import random
import time

# optional first step, define the driver, ie chrome or Brave
driver = webdriver.Chrome('./chromedriver')     # <- chromedriver needs to be the same version as chrome


url = "https://www.tripadvisor.com/Restaurants-g30196-Austin_Texas.html#EATERY_LIST_CONTENTS"

# url = "<a data-page-number="1" data-offset="0" href="/Restaurants-g30196-Austin_Texas.html#EATERY_LIST_CONTENTS" class="nav previous rndBtn ui_button primary taLnk" onclick="      require('common/Radio')('restaurant-filters').emit('paginate', this.getAttribute('data-offset'));; ta.trackEventOnPage('STANDARD_PAGINATION', 'previous', '1', 0); return false;
#   ">
# Previous
# </a>" //*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a
#//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/a
# #EATERY_LIST_CONTENTS > div.deckTools.btm > div > a
driver.get(url)

    # NEED TO LOOK AT WEBDRIVER DOCUMENTATION, THIS PROCESS IS NOT WORKING

# now lets narrow in on the data we want to collect
rest_dict = {'review_pages':[],'names':[]}

#driver.get(url)
#/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[2]/div/a
# retrieve the names and Trip Advisor links of all the restaraunts in the given city
def names_and_links(some_url,data_parameters):
    #print(data_parameters)
    # request the data from the desired page
    #page = driver.get(some_url)#,data=data_parameters)
    
    page = requests.get(some_url)
    
    # set encoding- this is the default so technically not necessary
    #page.encoding = 'ISO-885901'

    # collect your soup!
    soup = BeautifulSoup(page.text, 'html.parser')

    # can print the page output with this -> print(soup.prettify())

    boost_list = soup.find_all(class_ = "wQjYiB7z")

    count = 0

    for listing in boost_list:
        # identify and append the link to the reviews page
        if listing.text[0].isdigit():
            reviews_link = listing.find('a')['href']
            rest_dict['review_pages'].append(reviews_link)

        # clean and append the name of the restaraunt(checking for a digit at
        # the beginning excludes sponsored listings)
        
        if listing.text[0].isdigit():
            name = re.sub(r'\d+', '',listing.text)[2:].strip()
            rest_dict['names'].append(name)
            print(name)
            count += 1
            
    print(count)
    # identify the "next" button
    next_ = soup.find(class_ = 'unified pagination js_pageLinks')

    # if theres a next page available identify it
    button_identifier = " ".join(next_.find('span')['class'])

    if button_identifier != "nav next disabled":
        #next_page_link = next_.find('a')['href']
        #print(next_page_link)
        

        # wait 4 - 12 secs before next scrape
        print("\nWaiting...\n")
        time.sleep(random.randint(4,12))

        # # move to the next page of results
        # data_page = {}
        # next_page = requests.get('https://www.tripadvisor.com' + next_page_link,params=)

        # next_soup = BeautifulSoup(next_page.text, 'html.parser')

        #update data page parameters
        # count +=1
        # offset += 30

        # data_page["data-page-number"] += 1
        # data_page["data-offset"] += 30

        # data_page["data-page-number"] = str(count)
        # data_page["data-offset"] = str(offset)

        count = int(data_page["data-page-number"]) + 1
        offset = int(data_page["data-offset"]) + 30
        
        data_page["data-page-number"] = str(count)
        data_page["data-offset"] = str(offset)

        driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[2]/div').click()

        #now run the above search again
        names_and_links(some_url,data_page)

count = 1
offset = 0
data_page = {"data-page-number":str(count),"data-offset":str(offset),"href":"/Restaurants-g30196-oa60-Austin_Texas.html#EATERY_LIST_CONTENTS", "class":"nav next rndBtn ui_button primary taLnk", "onclick":f"      require('common/Radio')('restaurant-filters').emit('paginate', this.getAttribute('data-offset'));; ta.trackEventOnPage('STANDARD_PAGINATION', 'next', '{count}', 0); return false;"}
names_and_links(url,data_page)

# NEED TO IDENTIFY BY DATA-PAGE-NUMBER AND/OR DATAOFFSET

df = pd.DataFrame(rest_dict,data_page)

# df['Name'] = names
# df['Review_Page'] = review_pages

print(len(df))

df.to_csv('Austin_restaurants.csv')