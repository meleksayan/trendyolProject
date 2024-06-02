import requests
from bs4 import BeautifulSoup
import json

urls = [
    "https://www.trendyol.com/cok-satanlar?type=mostFavourite&webGenderId=1",
    "https://www.trendyol.com/cok-satanlar?type=bestSeller&webGenderId=1",
    "https://www.trendyol.com/cok-satanlar?type=mostRated&webGenderId=1",
    "https://www.trendyol.com/cok-satanlar?type=topViewed&webGenderId=1"
]

#A list that will hold all product information
product_list = []

for url in urls:
    # web page is requested
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # mark the area where the products are located
    products = soup.find_all("div", class_="product-card")

    for product in products:
        # the brand of each product is taken
        product_brand = product.find("span", class_="product-brand").text.strip()

        # the name of each product is taken
        product_name = product.find("span", class_="product-name").text.strip()

        # the price of each product is taken
        product_price = product.find("div", class_="prc-box-dscntd").text.strip()

        # the review of each product is taken
        review_count = product.find("span", class_="ratingCount").text.strip()
        

        rank_span = product.find("span", class_="rank-text")

        # taken the rank text
        if rank_span:
            rank = rank_span.text.strip()
        else:
            rank = "Bilgi Yok"
        
        # the link of each product is taken
        product_link = "https://www.trendyol.com" + product.find("a")["href"]

        # the seller  of each product is taken  from detail page
        detail_response = requests.get(product_link)
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")
        seller = detail_soup.find("span", class_="product-description-market-place").text.strip()
        
        # the link of each product is taken
        color_span = detail_soup.find("span", string="Renk")
        if color_span:
            color_value = color_span.find_next_sibling("span").text.strip()
        else:
            color_value = "Bilgi Yok"

        # the importance of the product
        is_featured = detail_soup.find("div", class_="category-top-rank-container")
        importance_text = is_featured.text.strip() if is_featured else "Düşük"

        # collect the information in the dictionary
        product_info = {
            "Ürün Adı": product_name,
            "Marka": product_brand,
            "Ürün Fiyatı": product_price,
            "Değerlendirme Sayısı": review_count,
            "Ürün Linki": product_link,
            "Satıcı": seller,
            "Renk": color_value,
            "Önem": importance_text,
            "Sıralama": rank
        }

        # add to list
        product_list.append(product_info)

# json loaded
with open("products.json", "w", encoding="utf-8") as f:
    json.dump(product_list, f, ensure_ascii=False, indent=4)

print("Ürün bilgileri 'products.json' dosyasına yazıldı.")
