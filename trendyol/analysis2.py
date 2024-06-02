import json
import matplotlib.pyplot as plt           #library
import mplcursors


#The Number of Products according to Brands (From Large to Small)(6)
def plot_brand_counts(products_data):
    # Calculating the number of products according to brands
    brand_counts = {}
    for product in products_data:
        brand = product["Marka"]
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

    # brand name and number of count 
    brands = list(brand_counts.keys())
    counts = list(brand_counts.values())

    # Sorting by the number of brands
    sorted_brands = [brand for _, brand in sorted(zip(counts, brands), reverse=True)]
    sorted_counts = sorted(counts, reverse=True)

    # Creating a column chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(sorted_brands, sorted_counts, color='skyblue')
    plt.title('The Number of Products according to Brands (From Large to Small)')
    plt.xlabel('Marka')
    plt.ylabel('Ürün Sayısı')
    plt.xticks(rotation=90)  # Printing brand names vertically

    # Function to show the text when hovering over each column
    def show_count(sel):
        idx = sel.target.index
        count = sorted_counts[idx]
        sel.annotation.set_text(f"{count} adet ürün")
        sel.annotation.get_bbox_patch().set(fc="white", ec="black", lw=1)

    mplcursors.cursor(bars, hover=True).connect("add", show_count)

    plt.tight_layout()  
    plt.show()

#The 10 Most Expensive Brands(7)
def plot_top_10_brands(products_data):
    # Collecting product prices by brands
    brand_prices = {}
    for product in products_data:
        brand = product.get("Marka", "Belirtilmemiş")  # If there is no brand information, mark it as 
        price = float(product.get("Ürün Fiyatı", "0").replace(" TL", "").replace(".", "").replace(",", "."))

        if brand in brand_prices:
            brand_prices[brand].append(price)
        else:
            brand_prices[brand] = [price]

    # Calculating average prices by brand
    average_prices = {brand: sum(prices) / len(prices) for brand, prices in brand_prices.items()}

    # Choosing the 10 most expensive brands
    top_10_brands = sorted(average_prices.keys(), key=lambda x: average_prices[x], reverse=True)[:10]
    top_10_prices = [average_prices[brand] for brand in top_10_brands]

    # Create a graphic
    plt.figure(figsize=(12, 8))
    bars = plt.barh(top_10_brands, top_10_prices, color='skyblue')
    plt.xlabel('Ortalama Fiyat (TL)')
    plt.ylabel('Marka')
    plt.title('The 10 Most Expensive Brands')

    # Adding interactive features
    cursor = mplcursors.cursor(bars, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        index = sel.target.index
        brand = top_10_brands[index]
        price = top_10_prices[index]
        sel.annotation.set_text(f"Marka: {brand}\nOrtalama Fiyat: {price:.2f} TL")

    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():
    file_path = "unique_products.json"                              #cleaned data (unique)
    with open(file_path, "r", encoding="utf-8") as f:
        products_data = json.load(f)


    #call the functions
    plot_brand_counts(products_data)
    plot_top_10_brands(products_data)

if __name__ == "__main__":
    main()
