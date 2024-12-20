from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://forms.gle/SE4RhBZ3xqzhFTdo6"

response = requests.get(URL)
response.raise_for_status()
zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")


properties = soup.find("ul", class_="List-c11n-8-84-3-photo-cards")
all_listing = properties.find_all("li")


links_list = []
address_list = []
price_list = []
for listing in all_listing:
    link = listing.find("a")
    price_tag = listing.find("span", class_="PropertyCardWrapper__StyledPriceLine")
    if link is not None:
        links_list.append(link.get("href"))
        address_list.append(link.find("address").get_text().strip().replace(" |",""))
        price = price_tag.get_text()
        for char in price:
            if char == "+" or char == "/" or char == " ":
                formatted_price = price.split(char)[0]
                price_list.append(formatted_price)
                break

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_option)


for i in range(len(links_list)):
    driver.get(FORM_URL)
    sleep(2)
    address_field = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_field = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_field = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_buttion = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address_field.send_keys(address_list[i])
    price_field.send_keys(price_list[i])
    link_field.send_keys(links_list[i])
    submit_buttion.click()

    if i == len(links_list) - 1:
        driver.quit()
