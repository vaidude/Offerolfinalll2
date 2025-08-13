import requests
from bs4 import BeautifulSoup

url = "https://www.lifestylestores.com/in/en/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

products = []
for item in soup.select(".product-item"):
    title = item.select_one(".product-title").text.strip()
    image = item.select_one("img")['src']
    price = item.select_one(".price").text.strip()
    products.append({"title": title, "image": image, "price": price})

print(products)
