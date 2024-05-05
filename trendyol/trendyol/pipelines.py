# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TrendyolPipeline:
    def open_spider(self, spider):
        # Oluşturulacak dosyaları aç
        self.file_products = open("products.json", "w")
        self.file_products.write("[\n")  
        self.products = []

    def close_spider(self, spider):
        # Dosyaları kapat
        product_lines = [
            "\t" + json.dumps(ItemAdapter(p).asdict())
            for p in self.products
        ]
        product_lines_joined = ",\n".join(product_lines)
        self.file_products.write(product_lines_joined)
        self.file_products.write("\n]\n")
        self.file_products.close() 

    def process_item(self, item, spider):
        # Item tipine göre işlemleri gerçekleştir
        if isinstance(item, Product): 
            self.products.append(item)
        return item