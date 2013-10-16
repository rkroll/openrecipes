from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem
from openrecipes.schema_org_parser import parse_recipes


class MarthastewartMixin(object):
    source = 'marthastewart'

    def parse_item(self, response):

      hxs = HtmlXPathSelector(response)
      raw_recipes = parse_recipes(hxs, {'source': self.source, 'url': response.url})

      return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class MarthastewartcrawlSpider(CrawlSpider, MarthastewartMixin):

    name = "marthastewart.com"

    allowed_domains = ["www.marthastewart.com"]

    start_urls = [
        "http://www.marthastewart.com/cook",
        "http://www.marthastewart.com/276948/dinner-tonight",
        "http://www.marthastewart.com/276954/great-cake-recipes",
        "http://www.marthastewart.com/276961/dinner-party-ideas",
        "http://www.marthastewart.com/1005841/martha%E2%80%99s-favorite-recipes-summer",
        "http://www.marthastewart.com/967078/recipe-collections",
    ]

    rules = (
      Rule(SgmlLinkExtractor(allow=('/.+')), callback='parse_item'),
    )
