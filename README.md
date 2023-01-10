# LuluHyperMarket Website Product  Details Webscraping

The code provided is a web scraper that extracts data about a product from a website. It makes an HTTP request to the specified URL and parses the HTML content of the response using the `scrapy` library.

### Requirements

- Python 3.8.0+
- Scrapy 2.7.1+
- requests



### Installation

A step by step guide on how to get the development environment running.

**1. Clone the repository**

     git clone https://github.com/Sagorhowlader/ecommerce-site-scrape

**2. Navigate to the project directory**

    cd ecommerce_site_scrape

**3. Install the dependencies**

    pip install -r requirements.txt


**5. Running the project**

    scrapy runspider main.py

**6. For save json in file run**

    scrapy runspider main.py -o data.json

`data.json` file save the data as 

```json
{
  "product_title": "PRODUCT TITLE",
  "product_price": "PRODUCT PRICE",
  "product_summary": "PRODUCT SUMMARY"[]
}
```

    