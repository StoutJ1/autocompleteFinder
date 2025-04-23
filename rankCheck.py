import requests
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
url = "https://www.amazon.com/b?node=133140011"


driver = webdriver.Firefox()
driver.get(url)
textSearch = driver.find_element("xpath","//*[@id=\"twotabsearchtextbox\"]")

def searchTermsFunc(searchTermList, searchLimiter, maxSearches):
    currentTermIndex = 0
    searchLimiter = searchLimiter
    action=ActionChains(driver)

    logData = open("log.txt", 'a+')

    while currentTermIndex < len(searchTermList):
        action.move_to_element(textSearch)
        action.click()
        textSearch.clear()
        action.send_keys(searchTermList[currentTermIndex]).perform()
        time.sleep(1)
        suggestions = driver.find_elements(By.CLASS_NAME,"s-suggestion")
        tempSuggestions = []
        if len(suggestions) == 1:
            print("Search dead end.")
        else:
            for i in range(len(suggestions)):
                if suggestions[i].get_attribute("aria-label") != None:
                    tempSuggestions.append(suggestions[i].get_attribute("aria-label"))
                    print(suggestions[i].get_attribute("aria-label"))
        currentTermIndex +=1
        for suggestionToCheck in tempSuggestions:
            if(suggestionToCheck.strip() not in searchTermList):
                searchTermList.append(suggestionToCheck.strip())
                print("Added:", suggestionToCheck.strip())                
        if((len(searchTermList) > searchLimiter) or currentTermIndex == len(searchTermList) or currentTermIndex == maxSearches ):
            print("Terminating Search, max search terms reached, end of search term list, or max searches completed.")
            print(searchTermList)
        
            for counterUpdate in range(len(searchTermList)):
                searchTermList[counterUpdate] = searchTermList[counterUpdate] + "\n"
                
            logData = open("log.txt", 'a+',encoding='utf-8')
            print(searchTermList)

            logData.writelines(searchTermList)
            logData.close()           
            break
 
    



            
searchTerms = ["cooking", "farming"]

searchTermsFunc(searchTerms,100,50)
