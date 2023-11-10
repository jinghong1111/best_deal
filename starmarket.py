import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome WebDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# URL to scrape
url = "https://www.starmarket.com/shop/search-results.html?q=meat&sort=&offerType=Y"
driver.get(url)

# Allow time for dynamic content to load (you may need to adjust the sleep duration)
time.sleep(5)

# Get the page source after dynamic content has loaded
page_source = driver.page_source

# Close the webdriver
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Extract data
product_titles = soup.find_all("div", class_="product-title")

# Create a CSV file and write header
csv_filename = "product_data.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = ["Item Number", "Name", "Price", "Image URL"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

    # Write data to CSV
    count = 0 
    for product_title in product_titles:
        product_name = product_title.find("a", class_="product-title__name")
        if product_name:
            product_name_text = product_name.text.strip()

            product_price_element = product_title.find("div", class_="product-title__qty")
            if product_price_element:
                product_price = product_price_element.text.strip()

                # Extract the image URL
                image_element = product_title.find("img", class_="ab-lazy")
                if image_element:
                    image_url = image_element.get("data-src", "")
                else:
                    image_url = ""

                # For simplicity, using a dummy item number (you may replace this with the actual item number logic)

                # Write data to CSV
                csv_writer.writerow({
                    "Item Number": count,
                    "Name": product_name_text,
                    "Price": product_price,
                    "Image URL": image_url
                })
                count+=1 

print(f"Data has been written to {csv_filename}")
