from scrapy import Spider
from scrapy.http import JsonRequest

from locations.categories import Extras, apply_yes_no
from locations.dict_parser import DictParser
from locations.hours import OpeningHours


class CaffeNeroGBSpider(Spider):
    name = "caffe_nero_gb"
    item_attributes = {"brand": "Caffe Nero", "brand_wikidata": "Q675808"}
    allowed_domains = ["caffenero-webassets-production.s3.eu-west-2.amazonaws.com"]
    start_urls = ["https://caffenero-webassets-production.s3.eu-west-2.amazonaws.com/stores/stores_gb.json"]

    def start_requests(self):
        for url in self.start_urls:
            yield JsonRequest(url=url)

    def parse(self, response):
        for location in response.json()["features"]:
            if (
                not location["properties"]["status"]["open"]
                or location["properties"]["status"]["opening_soon"]
                or location["properties"]["status"]["temp_closed"]
            ):
                continue

            item = DictParser.parse(location["properties"])
            item["geometry"] = location["geometry"]
            if location["properties"]["status"]["express"]:
                item["brand"] = "Nero Express"

            item["opening_hours"] = OpeningHours()
            for day_name, day_hours in location["properties"]["hoursRegular"].items():
                if day_hours["open"] == "closed" or day_hours["close"] == "closed":
                    continue
                if day_name == "holiday":
                    continue
                item["opening_hours"].add_range(day_name.title(), day_hours["open"], day_hours["close"])

            apply_yes_no(Extras.TAKEAWAY, item, location["properties"]["status"]["takeaway"], False)
            apply_yes_no(Extras.DELIVERY, item, location["properties"]["status"]["delivery"], False)
            apply_yes_no(Extras.WIFI, item, location["properties"]["amenities"]["wifi"], False)
            apply_yes_no(Extras.TOILETS, item, location["properties"]["amenities"]["toilet"], False)
            apply_yes_no(Extras.BABY_CHANGING_TABLE, item, location["properties"]["amenities"]["baby_change"], False)
            apply_yes_no(Extras.SMOKING_AREA, item, location["properties"]["amenities"]["smoking_area"], False)
            apply_yes_no(Extras.AIR_CONDITIONING, item, location["properties"]["amenities"]["air_conditioned"], False)
            apply_yes_no(Extras.WHEELCHAIR, item, location["properties"]["amenities"].get("disabled_access"), False)
            apply_yes_no(Extras.TOILETS_WHEELCHAIR, item, location["properties"]["amenities"]["disabled_toilet"], False)
            apply_yes_no(Extras.OUTDOOR_SEATING, item, location["properties"]["amenities"]["outside_seating"], False)

            yield item
