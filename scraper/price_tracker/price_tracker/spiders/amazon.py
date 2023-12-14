import scrapy
import json

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/gp/twister/dimension?isDimensionSlotsAjax=1&asinList=B0C27VNNWH&vs=1&productTypeDefinition=NOTEBOOK_COMPUTER&productGroupId=pc_display_on_website&isPrime=1&isOneClickEnabled=0&originalHttpReferer=https%3A%2F%2Fwww.amazon.in%2Fref%3Dnav_logo&deviceType=web&showFancyPrice=false&twisterFlavor=twisterPlusDesktopConfigurator"]

    def start_requests(self, ) :
        amzn_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Referer': f"https://www.amazon.in/dp/B0C27VNNWH/?_encoding=UTF8&ref_=pd_gw_deals_ct_t1",
            'Cookie': 'i18n-prefs=INR; ubid-acbin=262-9143999-8509443; lc-acbin=en_US',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'TE': 'trailers'
        }
        yield scrapy.Request(
            url="https://www.amazon.in/gp/twister/dimension?isDimensionSlotsAjax=1&asinList=B0C27VNNWH&vs=1&productTypeDefinition=NOTEBOOK_COMPUTER&productGroupId=pc_display_on_website&isPrime=1&isOneClickEnabled=0&originalHttpReferer=https%3A%2F%2Fwww.amazon.in%2Fref%3Dnav_logo&deviceType=web&showFancyPrice=false&twisterFlavor=twisterPlusDesktopConfigurator",
            headers=amzn_headers,
        )

    def parse(self, response):
        price_data = json.loads(response.text)

        try:
            price = int(float(price_data["Value"]["content"]["twisterSlotJson"]["price"]))
            ASIN = price_data["ASIN"]
            
            yield {
                "ASIN": ASIN,
                "price": price,
            }

        except ValueError:
            self.logger.error("AMAZON: Failed to scrape")
