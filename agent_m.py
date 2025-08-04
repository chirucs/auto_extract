import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

hotel_location = "lewisburg"
hotel_name_to_search = "Motel M"

# Setup Selenium WebDriver
options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.booking.com")

# Wait for the search box to appear (updated selector)
search_box = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='ss']"))
)
search_box.clear()
search_box.send_keys(hotel_location)

# Open the date picker and select today's date
checkin_date = datetime.now().strftime('%Y-%m-%d')
search_box.send_keys(Keys.ENTER)

# Wait for the results to load
WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='property-card']"))
)

# Find hotel names and prices from the search results
hotels = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='property-card']")
found = False
for hotel in hotels:
    name = hotel.find_element(By.CSS_SELECTOR, "div[data-testid='title'").text
    if hotel_name_to_search.lower() in name.lower():
        try:
            price = hotel.find_element(By.CSS_SELECTOR, "span[data-testid='price-and-discounted-price'], span[data-testid='price'").text
        except:
            price = "No price found"
        print(f"Hotel: {name} | Price: {price}")
        found = True
        break

if not found:
    print(f"Hotel '{hotel_name_to_search}' not found in the search results.")

# Update the script to extract the price for Motel M using the provided link and XPath
hotel_url = "https://www.booking.com/hotel/us/better-value-inn-lewisburg.html?aid=356980&label=gog235jc-10CAso7AFCGmJldHRlci12YWx1ZS1pbm4tbGV3aXNidXJnSDNYA2i2AogBAZgBM7gBB8gBDNgBA-gBAfgBAYgCAagCAbgCicbExAbAAgHSAiQ0MGFlNGRkOC1mMjUyLTRmM2QtOGNiOS01OTUxZTM1MDJjODPYAgHgAgE&sid=157865f0eb34cad3cb41f094afa68340&all_sr_blocks=42885303_202858532_2_0_0&checkin=2025-08-04&checkout=2025-08-05&dest_id=20147370&dest_type=city&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=42885303_202858532_2_0_0&hpos=1&matching_block_id=42885303_202858532_2_0_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&sr_pri_blocks=42885303_202858532_2_0_0__7593&srepoch=1754345661&srpvid=9de26beb0cc11c18840a0e2ab73f667f&type=total&ucfs=1&"
driver.get(hotel_url)

# Use the provided XPath to locate the price element
price_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[4]/main/div[1]/div[4]/div/div[5]/div[4]/div/form/div[8]/div[1]/table/tbody/tr[1]/td[2]/div/div[1]/div[1]/div[2]/div/span"))
)

# Extract the price
price = price_element.text
print(f"Price for Motel M: {price}")

driver.quit()
