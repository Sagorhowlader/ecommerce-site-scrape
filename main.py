import scrapy
from scrapy.linkextractors import LinkExtractor

class LuluHypermarketSpider(scrapy.Spider):
    name = 'lulu_hypermarket'
    start_urls = ['https://www.luluhypermarket.com/en-ae/electronics']

    def parse(self, response):
        # Find the container element that holds the subcategories and products
        container = response.css('div.section-container.recommended-content')
        # Extract the URLs for the subcategories and products
        subcategories_urls = container.css('a::attr(href)').extract()
        for subcategory_url in subcategories_urls:
            subcategory_url = response.urljoin(subcategory_url)
            yield scrapy.Request(subcategory_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        container = response.css('div.product-box')
        # Extract the URLs for the products
        products_urls = container.css('a::attr(href)').extract()
        for product_url in products_urls:
            product_url = response.urljoin(product_url)
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        # Extract the price
        price = response.css('div.price-tag.detail span.current span.item.price span::text').extract_first()
        # Extract the title
        title = response.css('h1.product-name::text').extract_first()
        # Extract the product summary
        summary = {}
        summary_description = response.css('div.description-block')
        summary_items = summary_description.css('li::text').getall()

        for summary_item in summary_items:
            print(summary_item)
        #     key = summary_item.css('div.key::text').extract_first()
        #     value = summary_item.css('div.value::text').extract_first()
        #     summary[key] = value
        #
        # yield {
        #     'price': price,
        #     'title': title,
        #     'summary': summary
        # }