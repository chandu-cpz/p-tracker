import scrapy
from selectolax.lexbor import LexborHTMLParser

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["www.flipkart.com"]
    start_urls = ["https://www.flipkart.com/ensure-complete-balanced-health-nutrition-drink/p/itm89ed79602371d?pid=ESRF3DZ2FYXRZ9XF"]

    def start_requests(self) :
        fk_headers= {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Host': 'www.flipkart.com'
        }
        
        yield scrapy.Request(
            url = "https://www.flipkart.com/ensure-complete-balanced-health-nutrition-drink/p/itm89ed79602371d?pid=ESRF3DZ2FYXRZ9XF",
            headers=fk_headers,
            meta={'impersonate': "chrome110"},
        )


    def parse(self, response):
        tree = LexborHTMLParser(response.text)
        price_data = tree.css_first("._30jeq3").text()[1:]
        try:
            price = int(price_data)
            name = tree.root.css_first(".B_NuCI").text()
            yield {
                "price": price,
                "name": name,
            }
        except ValueError:
            self.logger.error("FLIPKART: Unable to scrape")

