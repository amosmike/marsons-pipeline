from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.chrome.service import Service
import yaml
import os 
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Scraper:

    '''
    This class is a scraper that works only for scraping the Autocar website 

    Attributes:
        URL (str): The webpage url    
    
    '''

    def __init__(self, URL: str):
        os.environ['GH_TOKEN']= self.git_token() # Expires Fri, Jul 1 2022. 
        self.URL = URL

            # Firefox
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        self.driver = Firefox(service = Service(GeckoDriverManager().install()), options=options)

        self.driver.get(URL)
        sleep(3)
        self.driver.maximize_window() # Maximize webpage
        self.r = self.driver.page_source
        self.s = BeautifulSoup(self.r,'html.parser')
        sleep(2)

    def scrape(self):
        ALL_LINK = self.find_ventures_list()
        self.table_number()
        self.get_details(ALL_LINK)

    def find_ventures_list(self):

        '''

        Fuction that retrieves pub link, name, and address from container on webpage

        Attributes:
        -----------
        NONE

        Returns
        -------
        list
            All pubs name, location, address, and link found from html
        
        '''

        ALL_LINK = []
        TAG = self.s.find("div", class_="venues-list").find_all("a", recursive=False)

        for tag1 in TAG:
            link1 = tag1.get("href")
            link1 = urljoin(self.URL, link1)
            name1 = tag1.find("h3", class_="body__heading").get_text().strip()
            if "," in name1:
                name1 = '"' + name1 + '"'
            #name1 = name1.replace(",", "")
            #addr = tag1.find("p", class_="body__address").get_text().strip()
            addr_tag = tag1.find("p", class_="body__address")
            if addr_tag:
                addr = addr_tag.get_text().strip()
                if "," in addr:
                    addr = '"' + addr + '"'
            else:
                addr = "N/A"
            entry = name1 + "|" + addr + "|" + link1
            ALL_LINK.append(entry)

        return ALL_LINK

    def git_token(self, token = 'geckodriver_token.yaml'): 

        '''

        Fuction that inputs token needed for Firefoz driver

        Attributes:
        -----------
        NONE

        Returns
        -------
        NONE
        
        '''
        with open(token, 'r') as t:
            token = yaml.safe_load(t)

        TOKEN = token['TOKEN']

        return TOKEN

    def table_number(self):

        '''

        Fuction that inputs token needed for Firefoz driver

        Attributes:
        -----------
        NONE

        Returns
        -------
        NONE
        
        '''

        self.driver.get("https://order.marstons.co.uk/bluejay/order")
        sleep(2)
        table_num = self.driver.find_element(By.CLASS_NAME, 'input-form__input')
        table_num.send_keys(1)
        self.driver.find_element(By.CLASS_NAME, 'input-form__button-text').click()
        sleep(2)

    def get_details(self, ALL_LINK):

        '''

        Fuction that iterates through link list returned from 'find_ventures_list()' and retreives name, location, item name, item price, and opening hours.
        Function writes details to csv.

        Attributes:
        -----------
        ALL_LINK

        Returns
        -------
        NONE
        
        '''
        output = open("pub_data_result.csv","w", encoding="utf-8")

        for num, line in enumerate(ALL_LINK[:3]):
            line = line.strip()
            name, addr, link = line.split("|")
            link = link.strip("/")
            link = link + "/order"
            print(f"{num+1}---{link}---DONE")
            self.driver.get(link)
            sleep(2)

            try:
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/section[1]/div/div[2]/div/div/p').click()
                sleep(1)
            except:
                item_name = item_price = opentime = 'N/A'
                entry = name + "," + addr + "," + item_name + "," + item_price + "," + opentime
                print(entry, file=output)
                pass

            r1 = self.driver.page_source
            s1 = BeautifulSoup(r1,'html.parser')

            ### OPENING
            opentag = s1.find("span", class_="text text--bold")
            if opentag:
                opentime = opentag.get_text().strip()
            else:
                opentime = "N/A"

            ###
            ITEM_TAG = s1.find_all('li', class_="drawer__item")
            for item_tag in ITEM_TAG:
                item_name = item_tag.find("h3",class_="details__name").get_text().strip()
                item_name = item_name.replace(",", " ")
                item_price = item_tag.find("p",class_="details__price").get_text().strip()
                entry = name + "," + addr + "," + item_name + "," + item_price + "," + opentime
                print(entry, file=output)

        output.close()

        
if __name__ == "__main__":
    marson_scraper = Scraper("https://order.marstons.co.uk")
    marson_scraper.scrape()
    marson_scraper.driver.quit()
