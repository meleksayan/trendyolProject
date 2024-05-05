import scrapy

class ProductSpider(scrapy.Spider):
    name = 'product'
    start_urls = ['https://www.trendyol.com/']

    def parse(self, response):
        # Ana sayfadaki "Kadın" kategorisine tıkla
        yield scrapy.Request(url='https://www.trendyol.com/butik/liste/1/kadin', callback=self.parse_women_category)

    def parse_women_category(self, response):
        # "Kadın" kategorisindeki "Elbise" kategorisine tıkla
        yield scrapy.Request(url='https://www.trendyol.com/elbise-x-c56', callback=self.parse_product)

    

    def parse_product(self, response):
        products = response.css('div.p-card-chldrn-cntnr.card-border')
        for product in products:
            try:
                name = product.css('span.prdct-desc-cntnr-name.hasRatings::text').get()
                if not name:
                    name = product.css('span.prdct-desc-cntnr-name::text').get()
                name = name.strip() if name else 'no info'

                yield {
                    'brand': product.css('span.prdct-desc-cntnr-ttl::text').get(),
                    'name': name,
                    'price': product.css('div.prc-box-dscntd::text').get().replace('TL', ''),
                    'link': response.urljoin(product.css('a::attr(href)').get()),
                    'review' : product.css('span.ratingCount::text').get(),
                    
                    
                    

                }

            except:
                yield {
                    'brand': product.css('span.prdct-desc-cntnr-ttl::text').get(),
                    'name': 'no info',
                    'price': product.css('div.prc-box-dscntd::text').get().replace('TL', ''),
                    'review': '0'
                }