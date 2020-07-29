from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd

# optional first step, define the driver, ie chrome or Brave
driver = webdriver.Chrome('./chromedriver')     # <- chromedriver needs to be the same version as chrome



# request the data from the desired page
page = driver.get("https://www.walgreens.com/storelistings/storesbycity.jsp?requestType=locator&state=ID")

# set encoding- this is the default so technically not necessary
page.encoding = 'ISO-885901'

# collect your soup!
soup = BeautifulSoup(page.text, 'html.parser')

# can print the page output with this -> print(soup.prettify())

# now lets narrow in on the data we want to collect

boost_list = soup.find_all()#class_ = 'sportsbook-odds american default-color')
for i in boost_list[:2]:                        
  print('\n',i)

event_list = soup.find_all()
for i in event_list[:2]:
    print('\n',i)

print('\nlist type', type(boost_list))
print('\nlist length',len(boost_list))

example = boost_list[0] # a representative example
example_content = example.contents
print('\nall of example.contents',example_content)   # <- this prints the new odds 

more_example_content = example.contents[0]
print('\nattributes of one piece of example contents',more_example_content.attrs)



# why does this only return one boost cell? The others are collapsed- must uncollapse them

# what do the attributes mean? attributes can be accessed like dictionary keys, eg example_content['href']

# how do we extract the odds value? Use a combination of classes and attributes to access the desired values




# boost_list = soup.find_all(class_ = 'sportsbook-odds american default-color')
# for i in boost_list[:2]:                        
#   print('\nBOOsted cell body',i)

# event_list = soup.find_all(class_ = 'component-101__cell__name')
# for i in event_list[:2]:
#     print('\nEvent names',i)

# print('\nboost list type', type(boost_list))
# print('\nboost list length',len(boost_list))

# example = boost_list[0] # a representative example
# example_content = example.contents
# print('\nall of example.contents',example_content)   # <- this prints the new odds 

# more_example_content = example.contents[0]
# print('\nattributes of one piece of example contents',more_example_content.attrs)

