from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.microdata_parser import parse_recipes


def callback(loader, scope):
  print 'got it'

class MyrecipesMixin(object):
  source = 'myrecipes'


  def parse_item(self, response):
    raw_recipes = parse_recipes(response, {'source': self.source, 'url': response.url})
    return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class MyrecipescrawlSpider(CrawlSpider, MyrecipesMixin):
  name = "myrecipes.com"

  allowed_domains = ["www.myrecipes.com"]

  start_urls = [
    "http://www.myrecipes.com/recipe-finder/",
  ]

  rules = (
    Rule(SgmlLinkExtractor(allow=('/.+')), callback='parse_item',follow=True),
    # Rule(SgmlLinkExtractor(allow=('/recipes/(.+)/')), callback='parse_item'),
    # Rule(SgmlLinkExtractor(allow=('/recipes/(.+)')), callback='parse_item'),
  )
