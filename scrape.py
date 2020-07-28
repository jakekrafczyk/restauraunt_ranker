#from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd

# first, define the driver, ie chrome or Brave
#driver = webdriver.Chrome()

# request the data from the desired page
page = requests.get("https://sportsbook.draftkings.com/sports/oddsboosts?category=odds-boost-specials&subcategory=today%27s-boosts")

# set encoding- this is the default so technically not necessary
page.encoding = 'ISO-885901'

# collect your soup!
soup = BeautifulSoup(page.text, 'html.parser')

# can print the page output with this -> print(soup.prettify())

# now lets narrow in on the data we want to collect

boost_list = soup.find_all(class_ = 'sportsbook-boosted-cell__element-newodds')
for i in boost_list[:2]:                        # 'sportsbook-boosted-cell__body'
                                                # "sportsbook-odds american default-color"
                                                # sportsbook-boosted american default-color
  print('\nBOOsted cell body',i)

event_list = soup.find_all(class_ = 'component-101__cell__name')
for i in event_list[:2]:
    print('\nEvent names',i)

print('\nboost list type', type(boost_list))
print('\nboost list length',len(boost_list))

example = boost_list[0] # a representative example
example_content = example.contents
print('\nall of example.contents',example_content)

more_example_content = example.contents[0]
print('\nattributes of one piece of example contents',more_example_content.attrs)

# why does this only return one boost cell?

# what do the attributes mean?

# how do we extract the odds value?