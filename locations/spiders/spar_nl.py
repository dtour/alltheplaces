from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider


class SparNLSpider(SitemapSpider, StructuredDataSpider):
    name = "spar_nl"
    item_attributes = {"brand": "Spar", "brand_wikidata": "Q610492"}
    sitemap_urls = ["https://www.spar.nl/sitemap/stores.xml/"]
    sitemap_rules = [(r"/winkels/", "parse_sd")]
