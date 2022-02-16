from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from project import settings
from project.spiders.target_com import TargetComSpider


def run_spider():

    # Set the crawler settings
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # Initialize the crawler process
    crawler_process = CrawlerProcess(settings=crawler_settings)

    # Add the spider
    crawler_process.crawl(TargetComSpider)

    # Start the process and close it at finish
    crawler_process.start()
    crawler_process.stop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_spider()
