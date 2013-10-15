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
    ]

    rules = (
      Rule(SgmlLinkExtractor(allow=('/cook/.+'))),
      Rule(SgmlLinkExtractor(allow=('/.+')), callback='parse_item'),
    )
