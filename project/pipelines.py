class ProjectPipeline:

    def open_spider(self, spider):
        self.items = list()

    def process_item(self, item, spider):
        self.items.append(item.__dict__.get('_values'))
        return item

    def close_spider(self, spider):
        for item in self.items:
            print(item.get('title'))
