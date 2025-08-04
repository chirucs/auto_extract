import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

hotel_location = "lewisburg"
hotel_name_to_search = "Quality Inn"

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

# Navigate directly to the specific hotel link
hotel_url = "https://www.booking.com/hotel/us/quality-inn-lewisburg.html?aid=304142&label=gen173nr-10CAEoggI46AdIM1gEaLYCiAEBmAEzuAEHyAEM2AED6AEB-AEBiAIBqAIBuALdksTEBsACAdICJDlkMzViNzVhLWY5YmMtNGYwMy05YjAxLTVjM2VlOWNjNTM5MtgCAeACAQ&sid=20039999fac23c8b03172ab9310caab2&all_sr_blocks=635963311_249012782_2_1_0&checkin=2025-08-04&checkout=2025-08-05&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=635963311_249012782_2_1_0&hpos=1&matching_block_id=635963311_249012782_2_1_0&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=distance_from_search&sr_pri_blocks=635963311_249012782_2_1_0__14000&srepoch=1754335608&srpvid=9d040aa9795825ede817d61873a375c5&type=total&ucfs=1&"
driver.get(hotel_url)

# Use XPath to locate the price element
price_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div[4]/main/div[1]/div[4]/div/div[5]/div[4]/div/form/div[18]/div[1]/table/tbody/tr[1]/td[2]/div/div[1]/div[1]/div[2]"))
)

# Extract the price
price = price_element.text
print(f"Price for Quality Inn: {price}")

driver.quit()
