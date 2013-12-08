from scrapy.contrib.spiders import SitemapSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from openrecipes.spiders.epicurious_spider import EpicuriousMixin


class EpicuriousfeedSpider(SitemapSpider, EpicuriousMixin):
    """
    Uses the Epicurious recipes sitemap to get items.
    """
    name = "epicurious.sitemap"
    allowed_domains = [
        "epicurious.com"
    ]
    sitemap_urls = ['http://www.epicurious.com/sitemap.xml']

    sitemap_rules = [
      ('/recipes/food/views/[A-Za-z0-9_-]+', 'parse_item'),
      ]

    # def parse(self, response):
    #
    #     xxs = XmlXPathSelector(response)
    #     links = xxs.select("//item/*[local-name()='origLink']/text()").extract()
    #
    #     return [Request(x, callback=self.parse_item) for x in links]
