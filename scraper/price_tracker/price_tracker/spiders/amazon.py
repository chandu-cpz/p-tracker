import scrapy
import json
import pymongo
import logging
from price_tracker.items import PriceTrackerItem
from scrapy.utils.project import get_project_settings
from random import randint
from scrapy.utils.defer import maybe_deferred_to_future


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]

    def __init__ (self):
        settings = get_project_settings()
        mongodbURI = settings.get("MONGODB_URI")
        self.mongoDBClient =  pymongo.MongoClient(mongodbURI)
        self.db = self.mongoDBClient["p-tracker"]
        self.collection = self.db["amznproducts"]

    def start_requests(self, ) :
        pipeline = [
            {
                "$group": {
                    "_id": "$productID", 
                    "productName": { "$first": "$productName"}
                }
            },
            {
                "$project": {
                    "productID": "$_id",
                    "productName": 1, 
                    "_id": 0
                }
            }
        ]

        products = list(self.collection.aggregate(pipeline))

        batchSize = 10

        for i in range(0, len(products), batchSize):
            batch = products[i:i+batchSize]
            asin_list = [p["productID"] for p in batch]  
            name_list = [p["productName"] for p in batch]
            
            amzn_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'Accept': 'text/html,*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Referer': f"https://www.amazon.in/dp/{asin_list[randint(0,len(asin_list)-1)]}/?_encoding=UTF8&ref_=pd_gw_deals_ct_t1",
                'Cookie': 'i18n-prefs=INR; ubid-acbin=262-9143999-8509443; lc-acbin=en_US',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'TE': 'trailers'
            }

            yield scrapy.Request(
                url=f"https://www.amazon.in/gp/twister/dimension?isDimensionSlotsAjax=1&asinList={','.join(asin_list)}&vs=1&productTypeDefinition=NOTEBOOK_COMPUTER&productGroupId=pc_display_on_website&isPrime=1&isOneClickEnabled=0&originalHttpReferer=https%3A%2F%2Fwww.amazon.in%2Fref%3Dnav_logo&deviceType=web&showFancyPrice=false&twisterFlavor=twisterPlusDesktopConfigurator",
                headers=amzn_headers,
                meta={"names": name_list}
            )

    def parse(self, response):
        product_list = response.text.split("&&&")
        product_names= response.meta['names']
        for product,name in zip(product_list, product_names):
            product = json.loads(product)
            try:
                item = PriceTrackerItem()
                item["price"] = int(float(product["Value"]["content"]["twisterSlotJson"]["price"]))
                item["url"] = product["ASIN"]
                item["name"] = name

                yield item

            except ValueError:
                self.logger.error(f"AMAZON: Failed Scraping: {product['ASIN']}")
    
    async def closed(self,reason):
        await maybe_deferred_to_future( self.mailer.send(to= self.adminEmail,subject=f"Stats of {self.name} spider",body='Stats: \n%s' % str(self.crawler.stats.get_stats())))
