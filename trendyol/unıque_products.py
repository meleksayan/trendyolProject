import json

# Loading data from a JSON file
with open("products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)

# List of unique products (We will check by combining product link and brand information)
unique_products = set()
unique_products_data = []

for product in products_data:
    # combine the product link and brand information to check that the product is unique
    product_key = (product["Ürün Linki"], product["Marka"])
    
    # product has not been added before, let's add it to the list of unique products and update the product data
    if product_key not in unique_products:
        unique_products.add(product_key)
        unique_products_data.append(product)

# write the updated data to the JSON file
with open("unique_products.json", "w", encoding="utf-8") as f:
    json.dump(unique_products_data, f, ensure_ascii=False, indent=4)

print("Benzersiz ürünler 'unique_products.json' dosyasına yazıldı.")



