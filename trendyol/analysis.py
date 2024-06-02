import json
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_products(products_data):
    cleaned_products = []  
    seen_products = set()   
    for product in products_data:  
        # A unique identity of each product is created
        product_key = (product["Ürün Adı"], product["Marka"])  
        # If the product has not been seen before, it is added to the cleaned products and added to the set of observed products
        if product_key not in seen_products:  
            cleaned_products.append(product)  
            seen_products.add(product_key)    
    return cleaned_products

#Distribution of products by price(1)
def plot_price_distribution(cleaned_products):          
    #A dictionary representing price ranges is created and started with the initial value of each range 
    price_ranges = {"0-50": 0, "51-100": 0, "101-150": 0, "151-200": 0, "201-250": 0, "251-300": 0, "301+": 0}
    for product in cleaned_products:  
        try:
            price = float(product["Ürün Fiyatı"].replace(" TL", "").replace(".", "").replace(",", "."))  
            if price < 50:
                price_ranges["0-50"] += 1
            elif price < 100:
                price_ranges["51-100"] += 1
            elif price < 150:
                price_ranges["101-150"] += 1
            elif price < 200:
                price_ranges["151-200"] += 1
            elif price < 250:
                price_ranges["201-250"] += 1
            elif price < 300:
                price_ranges["251-300"] += 1
            else:
                price_ranges["301+"] += 1
        except ValueError:
            pass  

    # Tags and dimensions are being created
    labels = price_ranges.keys()  
    sizes = price_ranges.values()  

    plt.figure(figsize=(12, 6))

    #piechart created
    plt.subplot(121)
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)     #This parameter adds percentage values ​​to the pie slices(autopct mean)
    plt.title('Distribution of products by price')
    plt.axis('equal')

    total_products = sum(sizes)
    price_counts_text = '\n'.join([f"{label}: {count} ürün" for label, count in price_ranges.items()])
    plt.text(1.6, 0.5, f"Total product: {total_products}\n\nFiyat Aralıklarına Göre Ürün Sayıları:\n{price_counts_text}", fontsize=12, color='black', ha='left', va='center')
    #ha:horizental aligment    va:vertical aligment
    plt.tight_layout()
    plt.show()    #show the graph


#the number of products according to sellers and their average prices (Bubble Chart)(2)
def plot_bubble_chart(products_data):     
    seller_counts = {}
    seller_prices = {}

    #Seller and price information are taken for each product.
    for product in products_data:
        seller = product["Satıcı"]
        price = float(product["Ürün Fiyatı"].replace(" TL", "").replace(".", "").replace(",", "."))

        if seller in seller_counts:
            seller_counts[seller] += 1
            seller_prices[seller].append(price)
        else:
            seller_counts[seller] = 1
            seller_prices[seller] = [price]

    sellers = list(seller_counts.keys())
    counts = list(seller_counts.values())
    avg_prices = [np.mean(prices) for prices in seller_prices.values()]
    
    ## Sellers are sorted by the number of products.
    sorted_indexes = np.argsort(counts)[::-1]
    sorted_sellers = np.array(sellers)[sorted_indexes]
    sorted_counts = np.array(counts)[sorted_indexes]
    sorted_avg_prices = np.array(avg_prices)[sorted_indexes]

    #The  bubble chart chart is created.
    fig, ax = plt.subplots(figsize=(12, 8))
    bubble_sizes = sorted_counts * 10
    scatter = ax.scatter(sorted_sellers, sorted_avg_prices, s=bubble_sizes, alpha=0.5, color='purple')
    plt.xlabel('Satıcı')
    plt.ylabel('Ortalama Fiyat')
    plt.title('the number of products according to sellers and their average prices (Bubble Chart)')
    plt.xticks(rotation=90)
    ## The limit of the Y axis is determined.
    plt.ylim(0, 4000)
    
    #Interactive feature is added.
    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        seller = sorted_sellers[sel.target.index]
        price = sorted_avg_prices[sel.target.index]
        count = sorted_counts[sel.target.index]
        sel.annotation.set_text(f'Satıcı: {seller}\nOrtalama Fiyat: {price:.2f}\nÜrün Sayısı: {count}')

    plt.grid(True)
    plt.tight_layout()
    plt.show()

#The Number of Reviews, etc. Product Price (Colored According to Brands)(3)
def plot_scatter_chart(products_data):       
    # Colors are determined to match each brand with a unique color.
    brands = set(product["Marka"] for product in products_data)
    num_brands = len(brands)
    colors = plt.cm.tab10(np.linspace(0, 1, num_brands))

    # A dictionary is created in which the brand and color are matched.
    color_dict = {brand: colors[i] for i, brand in enumerate(brands)}

    prices = []
    review_counts = []
    brand_colors = []
    brand_names = []
    product_names = []

    #Price, number of reviews, brand and product name information are taken for each product.
    for product in products_data:
        try:
            price = float(product["Ürün Fiyatı"].replace(" TL", "").replace(".", "").replace(",", "."))
            review_count = int(product["Değerlendirme Sayısı"].replace("(", "").replace(")", "").replace(",", ""))
            prices.append(price)
            review_counts.append(review_count)
            brand = product["Marka"]
            brand_colors.append(color_dict[brand])
            brand_names.append(brand)
            product_names.append(product["Ürün Adı"])
        except ValueError:
            continue

    plt.figure(figsize=(6, 4))
    scatter = plt.scatter(review_counts, prices, c=brand_colors, alpha=0.7)
    plt.xlabel('Değerlendirme Sayısı')
    plt.ylabel('Ürün Fiyatı (TL)')
    plt.title('The Number of Reviews, etc. Product Price (Colored According to Brands)')
    plt.grid(True)   ## Add grid lines to the plot for better visualization of data points and trends



    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        index = sel.target.index
        brand = brand_names[index]
        price = prices[index]
        review_count = review_counts[index]
        product_name = product_names[index]
        sel.annotation.set_text(f"Ürün Adı: {product_name}\nMarka: {brand}\nDeğerlendirme Sayısı: {review_count}\nÜrün Fiyatı: {price} TL")

    plt.show()

#Plotting the popularity of colors based on the number of products available in each color.(4)
def plot_color_popularity(products_data):     
    color_counts = {}
    color_prices = {}
    color_max_brands = {}
    brand_counts = {}
    brand_prices = {}

    for product in products_data:
        color = product.get("Renk", "Belirtilmemiş")
        brand = product.get("Marka", "Belirtilmemiş")
        price = float(product.get("Ürün Fiyatı", 0).replace(" TL", "").replace(".", "").replace(",", "."))

        if color in color_counts:
            color_counts[color] += 1
            if color_prices[color] < price:
                color_prices[color] = price
                color_max_brands[color] = [brand]
            elif color_prices[color] == price:
                color_max_brands[color].append(brand)
        else:
            color_counts[color] = 1
            color_prices[color] = price
            color_max_brands[color] = [brand]

        if brand in brand_counts:
            brand_counts[brand] += 1
            if brand_prices[brand] < price:
                brand_prices[brand] = price
        else:
            brand_counts[brand] = 1
            brand_prices[brand] = price

    sorted_colors = sorted(color_counts.keys(), key=lambda x: color_counts[x], reverse=True)
    sorted_counts = [color_counts[color] for color in sorted_colors]

    plt.figure(figsize=(10, 8))
    bars = plt.barh(sorted_colors, sorted_counts, color='lightblue')

    plt.xlabel('Ürün Sayısı')
    plt.ylabel('Renk')
    plt.title('Popularity of colors')

    cursor = mplcursors.cursor(bars, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        index = sel.target.index
        color = sorted_colors[index]
        count = sorted_counts[index]
        price = color_prices[color]
        max_brands = ", ".join(color_max_brands[color])
        sel.annotation.set_text(f"{color}: {count} adet\nEn Yüksek Fiyat: {price:.2f} TL\nEn Yüksek Fiyatlı Ürün Markası: {max_brands}")

    plt.show()

#the 20 most evaluated products(5)
def plot_top_reviewed_products(products_data):       
    def extract_product_id(link):
        #"""Extracts the product ID from the product link."""
        return link.split("-p-")[-1].split("?")[0]

    product_review_counts = {}
    
    # Count the number of reviews for each product
    for product in products_data:
        product_id = extract_product_id(product.get("Ürün Linki", ""))
        review_count = int(product.get("Değerlendirme Sayısı", "0").replace("(", "").replace(")", "").replace(",", ""))
        if product_id not in product_review_counts:
            product_review_counts[product_id] = review_count
        else:
            product_review_counts[product_id] = max(product_review_counts[product_id], review_count)
    
    # Sort the product IDs based on review counts
    filtered_product_ids = list(product_review_counts.keys())
    filtered_review_counts = list(product_review_counts.values())

    sorted_indices = sorted(range(len(filtered_review_counts)), key=lambda k: filtered_review_counts[k], reverse=True)
    sorted_product_ids = [filtered_product_ids[i] for i in sorted_indices]
    sorted_review_counts = [filtered_review_counts[i] for i in sorted_indices]
    
    # Select the top 20 reviewed products
    sorted_product_ids = sorted_product_ids[:20]
    sorted_review_counts = sorted_review_counts[:20]

    #Plotting
    plt.figure(figsize=(10, 8))
    bars = plt.bar(sorted_product_ids, sorted_review_counts, color='skyblue')
    plt.xlabel('Ürün ID')
    plt.ylabel('Toplam Değerlendirme Sayısı')
    plt.title('the 20 most evaluated products')
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
 

    #üstüne gelinince gösterme:interaktif
    cursor = mplcursors.cursor(bars, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        index = sel.target.index
        product_id = sorted_product_ids[index]
        product_name = next((product.get("Ürün Adı", "Bilinmiyor") for product in products_data if extract_product_id(product.get("Ürün Linki", "")) == product_id), "Bilinmiyor")
        sel.annotation.set_text(f"Ürün Adı: {product_name}\nDeğerlendirme Sayısı: {sorted_review_counts[index]}")

    plt.show()

def main():
    file_path = "unique_products.json"          #it is cleaned json(unique)
    products_data = load_data(file_path)
    cleaned_products = clean_products(products_data)


    #call the functions
    plot_price_distribution(cleaned_products)
    plot_bubble_chart(products_data)
    plot_scatter_chart(products_data)
    plot_color_popularity(products_data)
    plot_top_reviewed_products(products_data)

if __name__ == "__main__":
    main()
