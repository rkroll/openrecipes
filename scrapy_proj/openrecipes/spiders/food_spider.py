from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.microdata_parser import parse_recipes

class FoodMixin(object):
    source = 'food'

    def parse_item(self, response):
        # skip review pages, which are hard to distinguish from recipe pages
        # in the link extractor regex
        if response.url.endswith('/review'):
            return []

        raw_recipes = parse_recipes(response, {u'source': self.source, 'url': response.url})

        return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]

class FoodSpider(CrawlSpider, FoodMixin):

    name = "food.com"

    allowed_domains = ["food.com"]

    start_urls = [
        'http://www.food.com/recipes',
        'http://www.food.com/recipe-finder/all?pn=1',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('/recipe-finder/all?pn=\d+'))),
        Rule(SgmlLinkExtractor(allow=('/recipes/.+'))),
        Rule(SgmlLinkExtractor(allow=('/recipe/.+')), callback='parse_item'),
    )
