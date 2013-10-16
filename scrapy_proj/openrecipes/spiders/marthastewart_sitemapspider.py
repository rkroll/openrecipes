from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders import SitemapSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from openrecipes.items import RecipeItem
from openrecipes.schema_org_parser import parse_recipes


class MarthastewartMixin(object):
  source = 'marthastewart'

  def parse_item(self, response):
    hxs = HtmlXPathSelector(response)
    raw_recipes = parse_recipes(hxs, {'source': self.source, 'url': response.url})

    return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class MarthastewartSitemapSpider(SitemapSpider, MarthastewartMixin):

  name = "marthastewart.sitemap"

  allowed_domains = ["marthastewart.com"]

  sitemap_urls = ['http://www.marthastewart.com/sitemap.xml']

  sitemap_rules = [
    ('/.+', 'parse_item'),
    ]