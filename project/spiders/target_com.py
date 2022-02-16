import json

import scrapy

from project.items import ProjectItem


class TargetComSpider(scrapy.Spider):
    name = 'target_com'
    allowed_domains = ['target.com']
    start_url = 'https://www.target.com/p/apple-iphone-13-pro-max/-/A-{}'
    info_url = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1' \
               '?key={}' \
               '&tcin={}' \
               '&pricing_store_id={}'
    questions_url = 'https://r2d2.target.com/ggc/Q&A/v1/question-answer' \
                    '?type=product' \
                    '&questionedId={}' \
                    '&page=0' \
                    '&size=10' \
                    '&sortBy=MOST_ANSWERS' \
                    '&key={}' \
                    '&errorTag=drax_domain_questions_api_error'
    product_id = '84616123'

    download_delay = 0.5

    def start_requests(self):
        yield scrapy.Request(url=self.start_url.format(self.product_id),
                             callback=self.parse)

    def parse(self, response, **kwargs):

        # Search for the JS script which has a json with the info to make the next requests
        chosen_js = None
        for js in response.xpath('//script/text()'):
            if '__PRELOADED_QUERIES__' in js.extract():
                chosen_js = js.extract()
                break

        if not chosen_js:
            return

        # Some replaces to parse the content into a json
        chosen_js = chosen_js[chosen_js.find('{'):].replace('undefined', '""').replace('new Set([])', '[]')

        json_content = json.loads(chosen_js).get('__PRELOADED_QUERIES__').get('queries')[0]

        # Extract the needed info to make the next request
        api_key = json_content[0][1].get('apiKey')
        pricing_store_id = json_content[0][1].get('pricing_store_id')

        yield scrapy.Request(url=self.info_url.format(api_key, self.product_id, pricing_store_id),
                             callback=self.parse_info,
                             meta={'api_key': api_key})

    def parse_info(self, response):
        api_key = response.meta.get('api_key')

        json_content = json.loads(response.text)

        for container in json_content.get('data').get('product').get('children'):
            # Description, highlights, specifications and title
            feature_container = container.get('item').get('product_description')

            highlights = feature_container.get('soft_bullets').get('bullets')

            specs = [spec.replace('<B>', '').replace('</B>', '') for spec in
                     feature_container.get('bullet_descriptions')]
            specifications = dict()
            for spec in specs:
                specifications[spec[:spec.find(':')]] = spec[spec.find(':') + 2:]

            description = feature_container.get('downstream_description')
            description = description[:description.find('<br')]

            title = feature_container.get('title')

            # Images
            image_container = container.get('item').get('enrichment').get('images')
            image_urls = list()
            image_urls.append(image_container.get('primary_image_url'))
            image_urls += image_container.get('alternate_image_urls')

            # Price
            price = container.get('price').get('current_retail')

            item = ProjectItem()
            item['title'] = title
            item['price'] = price
            item['description'] = description
            item['specifications'] = specifications
            item['highlights'] = highlights
            item['image_urls'] = image_urls

            yield scrapy.Request(url=self.questions_url.format(self.product_id, api_key),
                                 callback=self.parse_questions,
                                 dont_filter=True,
                                 meta={'item': item})

    def parse_questions(self, response):
        item = response.meta.get('item')

        json_content = json.loads(response.text)

        questions = dict()
        for container in json_content.get('results'):
            question = container.get('text')
            answers = [answer.get('text') for answer in container.get('answers')]
            questions[question] = answers

        item['questions'] = questions

        yield item
