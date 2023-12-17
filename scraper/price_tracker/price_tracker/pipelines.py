# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import motor.motor_asyncio
from bson.datetime_ms import DatetimeMS
import datetime
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings
import asyncio
import logging
from scrapy.utils.defer import maybe_deferred_to_future
import pymongo

class PriceTrackerPipeline:
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        settings = get_project_settings()
        self.mailer =  MailSender.from_settings(settings)
        self.adminEmail = settings["ADMIN_EMAIL"]
        self.userEmail = settings["USER_EMAIL"]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGODB_URI"),
        )

    def open_spider(self, spider):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_uri)
        self.db = self.client["scrapedData"]
        self.fk = self.db["flipkart"]
        self.amzn= self.db['amazon']
        spider.mailer = self.mailer
        spider.adminEmail = self.adminEmail

    def close_spider(self, spider):
        logging.info("Closing DB, MAIL CONN")
        self.client.close()
        spider.mongoDBClient.close()

    async def process_item(self, item, spider):
        if spider.name=="flipkart": 
            #Get Lasted Scraped Price
            try: 
                recent_price =await self.fk.find_one(
                    {"url": item["url"]},
                    sort=[("timestamp", pymongo.DESCENDING)], 
                    projection={"price": 1, "_id": 0}
                )
            except Exception as e:
                logging.error("Failed Fetching price from MongoDB")

            #Send Email
            if recent_price:
                price_drop = recent_price["price"] - item["price"]
                if price_drop > 0:
                    try:
                        logging.info(f"Price of {item['name']} Dropped")
                        
                        message = (f"Price of {item['name']} dropped!\n"
                            f"Previous Price: {recent_price['price']}\n"
                            f"Price Drop: {price_drop}\n"
                            f"Current Price: {item['price']}\n"
                            f"Purchase Link: {item['url']}"
                        )
                        await maybe_deferred_to_future(self.mailer.send(to= self.adminEmail,subject=f"Price of {item['name']} Dropped",body=message))
                        await maybe_deferred_to_future(self.mailer.send(to= self.userEmail,subject=f"Price of {item['name']} Dropped",body=message))
                    except Exception as e:
                        logging.error("Failed Sending Email", e)
            else:
                try:
                    new_product_message = (f" This is to inform that we started tracking {item['name']}\n"
                        f"Current Price: {item['price']}\n"
                        f"Purchase Link: {item['url']}"
                    )
                    logging.info(f"New Product: {item['name']}")
                    await maybe_deferred_to_future(self.mailer.send(to= self.adminEmail,subject="New Product",body=new_product_message))
                    await maybe_deferred_to_future(self.mailer.send(to= self.userEmail,subject="New Product",body=new_product_message))
                except Exception as e:
                    logging.error("Failed Sending Email", e)
            
            # Insert the newly scraped price into DB
            try:
                await self.fk.insert_one({
                "timestamp": DatetimeMS(datetime.datetime.now(tz=datetime.timezone.utc)),
                "name": item["name"],
                "price": item["price"],
                "url": item["url"],
            })
            except Exception as e:
                logging.error("Failed Inserting Scraped Data into DB")

        elif spider.name == "amazon": 
            #Get Lasted Scraped Price
            try: 
                recent_price =await self.amzn.find_one(
                    {"url": item["url"]},
                    sort=[("timestamp", pymongo.DESCENDING)], 
                    projection={"price": 1, "_id": 0}
                )
            except Exception as e:
                logging.error("Failed Fetching price from MongoDB")

            #Send Email
            if recent_price:
                price_drop = recent_price["price"] - item["price"]
                if price_drop > 0:
                    try:
                        logging.info(f"Price of {item['name']} Dropped")
                        
                        message = (f"Price of {item['name']} dropped!\n"
                            f"Previous Price: {recent_price['price']}\n"
                            f"Price Drop: {price_drop}\n"
                            f"Current Price: {item['price']}\n"
                            f"Purchase Link: https://www.amazon.in/dp/{item['url']}"
                        )
                        await maybe_deferred_to_future(self.mailer.send(to= self.adminEmail,subject=f"Price of {item['name']} Dropped",body=message))
                        await maybe_deferred_to_future(self.mailer.send(to= self.userEmail,subject=f"Price of {item['name']} Dropped",body=message))
                    except Exception as e:
                        logging.error("Failed Sending Email", e)
            else:
                try:
                    new_product_message = (f" This is to inform that we started tracking {item['name']}\n"
                        f"Current Price: {item['price']}\n"
                        f"Purchase Link: https://www.amazon.in/dp/{item['url']}"
                    )
                    logging.info(f"New Product: {item['name']}")
                    await maybe_deferred_to_future(self.mailer.send(to= self.adminEmail,subject="New Product",body=new_product_message))
                    await maybe_deferred_to_future(self.mailer.send(to= self.userEmail,subject="New Product",body=new_product_message))
                except Exception as e:
                    logging.error("Failed Sending Email", e)
            
            # Insert the newly scraped price into DB
            try:
                await self.amzn.insert_one({
                "timestamp": DatetimeMS(datetime.datetime.now(tz=datetime.timezone.utc)),
                "name": item["name"],
                "price": item["price"],
                "url": item["url"],
            })
            except Exception as e:
                logging.error("Failed Inserting Scraped Data into DB")

        return item

#Use this to create a timeseries collection   
# .create_collection(
#             "flipkart",
#             timeseries = {
#                 "timeField": "timestamp",
#                 "metaField": "url",
#             }
#         )