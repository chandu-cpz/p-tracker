import scrapy
from selectolax.lexbor import LexborHTMLParser
import pymongo
from scrapy.utils.project import get_project_settings
from price_tracker.items import PriceTrackerItem
from scrapy.utils.defer import maybe_deferred_to_future
import logging

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["www.flipkart.com"]
    
    def __init__ (self):
        settings = get_project_settings()
        mongodbURI = settings.get("MONGODB_URI")
        self.mongoDBClient =  pymongo.MongoClient(mongodbURI)
        self.db = self.mongoDBClient["p-tracker"]
        self.collection = self.db["fkproducts"]

    def start_requests(self) :
        urls = self.collection.distinct("productURL")  
        logging.info(f"FKRT: Scraping {len(urls)} products")
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
        
        for url in urls: 
            yield scrapy.Request(
            url = url,
            headers=fk_headers,
            meta={'impersonate': "chrome110"},
            )


    def parse(self, response):
        tree = LexborHTMLParser(response.text)
        try:
            item = PriceTrackerItem()
            item["name"] =  str(tree.root.css_first(".B_NuCI").text().replace('\xa0', ''))
            item["price"] = int(tree.css_first("._30jeq3").text()[1:].replace(",",""))
            item["url"] = response.url
            yield item
        except ValueError:
            logging.error(f"Failed Scraping: {response.url}")

    async def closed(self,reason):
        await maybe_deferred_to_future( self.mailer.send(to= self.adminEmail,subject=f"Stats of {self.name} spider",body='Stats: \n%s' % str(self.crawler.stats.get_stats())))