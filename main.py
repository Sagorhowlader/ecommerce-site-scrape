import re

import scrapy


def clean_string(string):
    """This function takes in a string and returns a cleaned version of that string. It removes leading and trailing
    whitespace, replaces non-breaking spaces with regular spaces, replaces hyphens with spaces, removes commas,
    and removes any remaining unnecessary characters."""

    # Strip leading and trailing whitespace
    string = string.strip()

    # Replace non-breaking spaces with regular spaces
    string = string.replace("\u00a0", " ")

    # Replace hyphens with spaces
    string = string.replace("–", " ")

    # Remove commas
    string = string.replace(",", "")

    # Remove any remaining unnecessary characters
    string = re.sub(r'[^\w\s\.\']', '', string)

    return string


class LuluHypermarketSpider(scrapy.Spider):
    # The name attribute in the LuluHypermarketSpider class is used to give the spider a unique identifier.
    name = 'lulu_hypermarket'

    # start_urls is a list of URLs that the spider will begin to crawl from
    start_urls = ['https://www.luluhypermarket.com/en-ae/electronics']

    def parse(self, response):
        """This is the main parsing function for the LuluHypermarketSpider spider. It extracts the URLs for the
        subcategories and products from the provided response and yields a request for each subcategory URL,
        calling the parse_subcategory function for each subcategory"""

        # Find the container element that holds the subcategories and products
        container = response.css('div.section-container.recommended-content')
        # Extract the URLs for the subcategories and products
        subcategories_urls = container.css('a::attr(href)').extract()
        for subcategory_url in subcategories_urls:
            subcategory_url = response.urljoin(subcategory_url)
            yield scrapy.Request(subcategory_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        """This function extracts the URLs for the products from the provided response and yields a request for each
        product URL, calling the parse_product function for each product."""
        container = response.css('div.product-box')
        # Extract the URLs for the products
        products_urls = container.css('a::attr(href)').extract()
        for product_url in products_urls:
            product_url = response.urljoin(product_url)
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        """This function extracts the product title, price, and summary from the provided response and stores them in
        a dictionary. It then yields the dictionary as the final output."""

        # Extract the product details container
        product_description = response.css('.product-description')

        # Extract the product title
        product_title = product_description.css('h1.product-name::text').extract_first()

        # Extract the product price
        price = product_description.css('div.price-tag span.current span.item.price span::text').extract_first()

        # Extract the product summary container
        description_block = product_description.css('.description-block')

        # Extract summary details in list
        description_items = description_block.css('li::text').extract()

        # Clean summary details string
        product_summary = [clean_string(item) for item in description_items if item is not None]

        # Create a dictionary to hold the extracted data
        product_data = {
            'product_title': clean_string(product_title) if product_title is not None else None,
            'product_price': price,
            'product_summary': product_summary
        }

        # Yield the data as a dictionary
        yield product_data
