from scrapy.contrib.spiders import SitemapSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from openrecipes.items import RecipeItem
from openrecipes.microdata_parser import parse_recipes


class Food52Mixin(object):
  source = 'Food52'

  def parse_item(self, response):
    hxs = HtmlXPathSelector(response)
    raw_recipes = parse_recipes(response, {'source': self.source, 'url': response.url})

    return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class Food52SitemapSpider(SitemapSpider, Food52Mixin):

  name = "food52.sitemap"

  allowed_domains = ["food52.com"]

  sitemap_urls = ['http://food52.com/sitemap-index.xml']

  sitemap_rules = [
    ('/recipes/.+', 'parse_item'),
    ]