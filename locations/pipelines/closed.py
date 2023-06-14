from scrapy import Spider

from locations.items import Feature


class ClosePipeline:
    closed_labels = ["closed", "coming soon"]

    def process_item(self, item: Feature, spider: Spider):
        if name := item.get("name"):
            for label in self.closed_labels:
                if label in name.lower():
                    spider.crawler.stats.inc_value("atp/closed_check")
                    spider.logger.warn(f'Found {label} in {name} ({item.get("ref")})')
                    break

        return item