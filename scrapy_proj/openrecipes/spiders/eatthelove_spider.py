from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from openrecipes.items import RecipeItem
from openrecipes.microdata_parser import parse_recipes


class EattheloveMixin(object):
    source = 'eatthelove'

    def parse_item(self, response):
        raw_recipes = parse_recipes(response, {'source': self.source, 'url': response.url})

        return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class EatthelovecrawlSpider(CrawlSpider, EattheloveMixin):

    name = "eatthelove.com"

    allowed_domains = ["www.eatthelove.com"]

    start_urls = [
        "http://www.eatthelove.com/recipe-archive/",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/\d\d\d\d/\d\d/.+/')),
             callback='parse_item'),
    )
