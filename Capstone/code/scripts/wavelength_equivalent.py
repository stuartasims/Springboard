#!/usr/bin/env python
# coding: utf-8

# In[28]:


def wavelength_equivalent(input_list):
    """fetch color hex values based on light wavelength values"""
    import pandas as pd
    import time
    if not input_list:
        print('Function was passed an empty list. No results generated')

    else:

        #get to web and page
        colorlist = []
        from selenium import webdriver

        #create session and navigate to page
        driver = webdriver.Chrome(
            executable_path=
            'C:/Users/Stuart/Documents/GitHub/DataScience/code/scripts/chromedriver.exe'
        )
        driver.get('https://www.johndcook.com/wavelength_to_RGB.html')
        driver.implicitly_wait(3)

        #set xpath values for page navigation
        input_value = '/html/body/div/p[3]/input[1]'
        convert_button = '/html/body/div/p[3]/input[2]'
        result = '/html/body/div/p[4]'

        #loop through wavelengths, store hex color code, clear input, and repeat
        for element in input_list:
            driver.find_element_by_xpath(input_value).send_keys(str(element))
            driver.find_element_by_xpath(convert_button).click()
            a = driver.find_element_by_xpath(result)
            color = a.text
            color_hex = color.partition('#')[2]
            colorlist.append(color_hex)
            time.sleep(1)
            driver.find_element_by_xpath(input_value).clear()

        #close the driver after looping
        driver.quit()

    return colorlist

