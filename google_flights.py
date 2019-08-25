# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 09:03:47 2019

@author: enes
"""
from selenium import webdriver
import pandas as pd
import pdb
import time
from selenium.webdriver.common.keys import Keys

def get_driver():
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)

driver = get_driver()

link='https://www.google.com/flights#flt'
driver.get(link)
driver.implicitly_wait(10)

with open('segment_list.csv', 'r') as f:
    lines = f.readlines()

# breakpoint()

# Scroll to bottom of the page for changing currency to USD
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

currency_button= driver.find_element_by_xpath(
                             '//*[@id="flt-app"]/div[2]/footer/div[2]/div[1]/hairline-button[3]'
                             )
currency_button.click()
time.sleep(5)
driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_UP)

usd_button = driver.find_element_by_xpath(
                             '//div[@jsinstance="0" and @data-flt-ve="currency"]'
                            )
usd_button.click()
time.sleep(3)
counter=0
for trip in lines:
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+Keys.HOME)
    driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[4]/div[2]/div/div[1]/div[2]/div[1]').click()
    time.sleep(5)
    fly_from=driver.find_element_by_xpath('//input[@placeholder="Nereden?"]')
    #time.sleep(5)
    fly_from.send_keys(trip.split(',')[0])
    
    driver.implicitly_wait(5)

    driver.find_element_by_xpath('//*[@id="sbse0"]/div[1]').click()
    time.sleep(5)
    
    driver.find_element_by_xpath('//*[@id="flt-app"]/div[2]/main[4]/div[2]/div/div[1]/div[2]/div[2]').click()
    time.sleep(5)
    fly_to=driver.find_element_by_xpath('//input[@placeholder="Nereye?"]')
    time.sleep(5)
    fly_to.send_keys(trip.split(',')[1])
    
    driver.find_element_by_xpath(
            '//*[@id="sbse0"]/div[1]').click()
    time.sleep(3)    
    # Selecting dates from list
    driver.find_element_by_xpath(
            '//*[@data-flt-ve="departure_date" and @role="presentation"]'
            ).click()
    driver.find_element_by_xpath(
            '//input[@placeholder="Kalkış tarihi"]'
            ).send_keys(trip.split(',')[2])
    driver.find_element_by_xpath(
            '//input[@placeholder="Dönüş tarihi"]'
            ).send_keys(trip.split(',')[3])
    driver.find_element_by_xpath(
        '//*[@id="flt-modaldialog"]/div/div[5]/g-raised-button/div'
        ).click()
    
    # Assign segment city values to variables for writing the name of output file. 
    origin = trip.split(',')[0]
    destination = trip.split(',')[1]
    
    time.sleep(10) 
    if counter == 0:
        more_button = driver.find_element_by_xpath(
                "//a[@class='gws-flights-results__dominated-link']"
                )
        driver.implicitly_wait(5)
    
        driver.execute_script("arguments[0].scrollIntoView();", more_button)
        driver.implicitly_wait(5)
        time.sleep(10) 
        more_button.click()
        driver.implicitly_wait(5)
        counter+=1
    time.sleep(10)
    vals = driver.find_elements_by_class_name(
        'gws-flights-results__result-item')
    results = []    
    for val in vals:
        result = dict()
        result['time'] = val.find_element_by_class_name(
            'gws-flights-results__times'
        ).text
        result['airports'] = val.find_element_by_class_name(
            'gws-flights-results__airports'
            ).text
        result['ellipsize'] = val.find_element_by_class_name(
                'gws-flights__ellipsize'
        ).text
        result['duration'] = val.find_element_by_class_name(
                'gws-flights-results__duration'
        ).text

        try:
            result['price'] = val.find_element_by_class_name(
                    'gws-flights-results__price'
            ).text
        except Exception:
            continue

        result['summary'] = val.find_element_by_class_name(
                'gws-flights-results__itinerary-card-summary').text
        result['airlines'] = val.find_element_by_class_name(
                'gws-flights-results__airline-extra-info'
                ).text
        result['stops']= val.find_element_by_class_name(
                'gws-flights-results__stops').text
        # print(result)
        results.append(result)

    df=pd.DataFrame(results)
    df.to_excel(origin + '_' + destination + '.xlsx')
    
