from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import sys

def validate_url(url):
    req = requests.get(url)
    if req.status_code == 200:
        return
    else:
        print(f"{url}\nUrl is unreachable. Exiting...")
        sys.exit()

def get_report(soup):
    all_div = soup.find("div",{"id":"mg-hover-info"})
    text = all_div.text
    report = text.split("  ")
    report = [i for i in report if i]
    return report

def print_report(city,report):
    print("-"*10)
    print("Kaupunki: " + city)
    print("Tämän päivän sää:")
    print(*report,sep="\n")
    print("-"*10)

def set_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_experimental_option('excludeSwitches',['enable-logging'])
    return chrome_options

if __name__ == '__main__':
    #set options to browser
    browser = webdriver.Chrome(options=set_options())

    #Choose a city in Finland.
    city = input("Choose a Finnish city: ").capitalize()
    url = "https://www.foreca.fi/Finland/" + city

    #Validate Url
    validate_url(url)
    print(f"Getting the weather from:\n{url}")
    browser.get(url)
    html = browser.page_source
    browser.quit()

    soup = BeautifulSoup(html, "html.parser")
    report = get_report(soup)
    print_report(city,report)