import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv
from datetime import datetime

# Mock conversion rate
GBP_TO_KES = 160

# URL to scrape
URL = "https://books.toscrape.com/catalogue/page-1.html"

# Lists to store data
books = []

def scrape_books(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad response
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all book containers
        book_items = soup.select('.product_pod')

        for item in book_items[:10]:  # Limit to 10 books
            title = item.h3.a['title']
            price_str = item.select_one('.price_color').text.strip()
            price_gbp = float(price_str[1:])  # Remove '£'
            price_kes = round(price_gbp * GBP_TO_KES, 2)

            books.append({
                'Title': title,
                'Price (GBP)': price_gbp,
                'Price (KES)': price_kes
            })

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")

def save_to_csv(data, filename='books_converted.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"\n✅ Data saved to {filename}")

def display_table(data):
    print("\n📚 Book Prices (Converted):\n")
    print(tabulate(data, headers="keys", tablefmt="grid"))

# Main flow
scrape_books(URL)
if books:
    display_table(books)
    save_to_csv(books)
    print(f"\n🕒 Conversion done at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
