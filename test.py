import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv
from datetime import datetime

# Mock conversion rate
USD_TO_KES = 130

# Mock URL or local HTML page (change as needed)
URL = "https://cars.toscrape.mock/page-1.html"  # Replace with real site if you get one

# Sample for testing (use this instead of the requests.get)
mock_html = """
<html><body>
<div class="car">
    <h2 class="car-name">Toyota Premio</h2>
    <span class="price">$8000</span>
</div>
<div class="car">
    <h2 class="car-name">Mazda Axela</h2>
    <span class="price">$7500</span>
</div>
<div class="car">
    <h2 class="car-name">Subaru Impreza</h2>
    <span class="price">$9500</span>
</div>
</body></html>
"""

cars = []

def scrape_cars():
    try:
        # soup = BeautifulSoup(requests.get(URL).text, 'html.parser')  # Use for real site
        soup = BeautifulSoup(mock_html, 'html.parser')  # For testing

        car_items = soup.select('.car')

        for item in car_items:
            name = item.select_one('.car-name').text.strip()
            price_str = item.select_one('.price').text.strip()
            price_usd = float(price_str.replace('$', ''))
            price_kes = round(price_usd * USD_TO_KES, 2)

            cars.append({
                'Car Name': name,
                'Price (USD)': price_usd,
                'Price (KES)': price_kes
            })

    except requests.RequestException as e:
        print(f"Error fetching car data: {e}")

def save_to_csv(data, filename='cars_converted.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"\n✅ Data saved to {filename}")

def display_table(data):
    print("\n🚗 Car Prices (Converted):\n")
    print(tabulate(data, headers="keys", tablefmt="grid"))

# Main flow
scrape_cars()
if cars:
    display_table(cars)
    save_to_csv(cars)
    print(f"\n🕒 Conversion done at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
