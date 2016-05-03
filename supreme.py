import time
import sys
import requests
from bs4 import BeautifulSoup
from splinter import Browser

mainUrl = "http://www.supremenewyork.com/shop/all"
baseUrl = "http://supremenewyork.com"
#productUrl = "http://www.supremenewyork.com/shop/t-shirts/morrissey-tee/white"
checkoutUrl = "https://www.supremenewyork.com/checkout"

# product info - input keyword as first argument
product = sys.argv[1]
selectOption = "Medium" # change this to the size you want

# billing/shipping info
namefield = "Name Name"
emailfield = "email@email.com"
phonefield = "0000000000"
addressfield = "00000 Zero Street"
zipfield = "00000"
statefield = "CA"
cctypefield = "master"  # "master" "visa" "american_express"
ccnumfield = "000000000000" # this is random, not my info lol
ccmonthfield = "00"
ccyearfield = "0000"
cccvcfield = "000"

# checks main shop url for name of product
def main():
    r = requests.get(mainUrl).text
    if "This page cannot be found" in r:
        print("Page could not be found")
        return
    print("Looking for: " + product)
    if product in r:
        print("The item is here!")
        parse(r)

# Parses all the links
def parse(r):
    soup = BeautifulSoup(r, "html.parser")
    for a in soup.find_all('a', href=True):
        link = a['href']
        checkproduct(link)

# Check if product name is in url
def checkproduct(l):
    if product in l:
        if color in l:
            prdurl = baseUrl + l
            print(prdurl)
            buyprd(prdurl)

# Open browser with the url and buy
def buyprd(prdurl):
    browser = Browser('firefox')
    browser.visit(prdurl)
    time.sleep(.5)
    print(browser.title)
    browser.find_option_by_text(selectOption).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added to Cart")
    else:
        print("Error")
        return

    time.sleep(2)
    print("checking out")
    browser.visit(checkoutUrl)
    time.sleep(.5)
    print("Filling Out Billing Info")
    browser.fill("order[billing_name]", namefield)
    browser.fill("order[email]", emailfield)
    browser.fill("order[tel]", phonefield)

    print("Filling Out Address")
    browser.fill("order[billing_address]", addressfield)
    browser.fill("order[billing_zip]", zipfield)
    browser.select("order[billing_state]", statefield)
    print("Filling Out Credit Card Info")

    browser.select("credit_card[type]", cctypefield)
    browser.fill("credit_card[number]", ccnumfield)
    browser.select("credit_card[month]", ccmonthfield)
    browser.select("credit_card[year]", ccyearfield)
    browser.fill("credit_card[verification_value]", cccvcfield)

    browser.find_by_css('.terms').click()
    time.sleep(.2)
    print("Submitting Info")
    browser.find_by_name('commit').click()
    time.sleep(1)

    browser.driver.save_screenshot('confirmation.png')
    print("Exiting...")
    time.sleep(2)
    sys.exit(0)

i = 0

while (True):
    test(mainUrl)
    print("On try number " + str(i))
    i = i + 1
    time.sleep(8)
