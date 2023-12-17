import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from price_tracker.spiders.amazon import AmazonSpider
from price_tracker.spiders.flipkart import FlipkartSpider

settings = get_project_settings()
process = CrawlerProcess(settings)

process.crawl(AmazonSpider)
process.crawl(FlipkartSpider)

process.start()
