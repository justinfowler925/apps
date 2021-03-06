import os, time, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# going to work with local files and chromedriver so we initialize here
currentDirectory = os.path.dirname(os.path.realpath(__file__))
driverPath = currentDirectory + "\\drivers\\chromedriver.exe"

# opens browser isntance of target site
browser: WebDriver = webdriver.Chrome(driverPath)
browser.get("https://minimarket.fldfs.com")

# open my target local file and write headers
with open('AgencyPolicies.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows([["Class", "Agency", "PolicyCount"]])

# using this variable for test should make this iterate with range 1-700
NUMBER_OF_ARROWS_DOWN = 700

# going to loop through and grab just the data we want
KEEP_GOING = True
while KEEP_GOING:
    classiwant = browser.find_elements_by_xpath("//div/input")
    classiwant[0].clear()
    classiwant[0].send_keys('0')

    # have to wait for option to appear in browser then scroll through object
    time.sleep(5)
    tempNumberArrowsDown = 1

    # need this loop to run through data form previously designated start number
    while tempNumberArrowsDown <= NUMBER_OF_ARROWS_DOWN:
        classiwant[0].send_keys(Keys.ARROW_DOWN)
        tempNumberArrowsDown += 1

    classiwant[0].send_keys(Keys.RETURN)
    allButtonsArray = browser.find_elements_by_xpath("//div/button")
    searchTerm = classiwant[1].get_attribute('value').strip().rstrip()
    allButtonsArray[2].click()
    print('Submitted Search')

    # need to insert another pause for table to load in browser, supress errors and grabe table
    time.sleep(10)
    ignored_exceptions = (NoSuchElementException, NameError)
    checkfortable = browser.find_elements_by_class_name('alert-danger')
    print([checkfortable])

    # message to user if table pull was found on page or not
    if len(checkfortable) > 0:
        print('No tables skipping to next code')
    else:
        print('Getting table')


        MORE_NEXT_PAGES = True
        while MORE_NEXT_PAGES:

            # Grab HTML table with results and confirm successful pull
            time.sleep(15)
            tableHtml = browser.find_element_by_id('tbl_results').get_attribute('innerHTML')
            print('table is working')
            soup = BeautifulSoup(tableHtml, 'html.parser')
            ALL_ROWS = soup.findAll('tr')
            startRow = 1
            data = []

            while startRow < len(ALL_ROWS):
                row = ALL_ROWS[startRow]
                agencyName = str(row.findAll('td')[0].contents[0]).strip().rstrip()
                policyCount = str(row.findAll('td')[1].contents[0]).strip().rstrip()
                data.append([searchTerm, agencyName, policyCount])
                startRow += 1
            with open('AgencyPolicies.csv', 'a', newline='') as fp:
                a = csv.writer(fp, delimiter=',')
                a.writerows(data)

            # Wait for pagination to appear to advance through pages
                time.sleep(10)
                ignored_exceptions = (NoSuchElementException, NameError,)
                PageNotReady = browser.find_elements_by_id('pagination')
                print([PageNotReady])

                if len(PageNotReady) < 1:
                    print('can not find pagination')
                    MORE_NEXT_PAGES = False
                else:
                    print('waiting for pagination')
                    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
                    pagination = WebDriverWait(browser, 100).until(
                        EC.presence_of_element_located((By.ID, "pagination")))
                    pagination = browser.find_elements_by_id('pagination')
                    listOfPaginationButtons = browser.find_elements_by_xpath("//*[contains(text(), 'Next')]")

                    if len(listOfPaginationButtons) > 0:
                        listOfPaginationButtons[0].click()
                    else:
                        print('cannot find the next button')
                        # We are done with this classification increment Arrows Down and go to next
                        MORE_NEXT_PAGES = False

    NUMBER_OF_ARROWS_DOWN += 1
    print([NUMBER_OF_ARROWS_DOWN])

# Success! Let user know project finished
print('all the way done')
