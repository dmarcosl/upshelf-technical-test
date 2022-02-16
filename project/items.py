import scrapy


class ProjectItem(scrapy.Item):
    price = scrapy.Field()
    description = scrapy.Field()
    specifications = scrapy.Field()
    highlights = scrapy.Field()
    questions = scrapy.Field()
    image_urls = scrapy.Field()
    title = scrapy.Field()
