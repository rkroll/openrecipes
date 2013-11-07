from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders import SitemapSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from openrecipes.items import RecipeItem
from openrecipes.microdata_parser import parse_recipes


class FoodnetworkMixin(object):
  source = 'foodnetwork'

  def parse_item(self, response):
    hxs = HtmlXPathSelector(response)
    raw_recipes = parse_recipes(response, {'source': self.source, 'url': response.url})

    return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class FoodnetworkSitemapSpider(SitemapSpider, FoodnetworkMixin):

  name = "foodnetwork.sitemap"

  allowed_domains = ["foodnetwork.com"]

  sitemap_urls = ['http://www.foodnetwork.com/food_sitemap_index.xml']

  sitemap_rules = [
    ('/recipes/.+', 'parse_item'),
    ]