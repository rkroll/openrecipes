from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import XmlXPathSelector
from scrapy.selector import HtmlXPathSelector
from scrapy import log
from openrecipes.spiders.marthastewart_spider import MarthastewartMixin


class MarthastewartfeedSpider(BaseSpider, MarthastewartMixin):
    """
    This parses the RSS feed for marthastewart.com, grabs the original
    links to each entry, and scrapes just those pages. This should be used
    to keep up to date after we have backfilled the existing recipes by
    crawling the whole site
    """
    name = "marthastewart.feed"

    allowed_domains = [
        "marthastewart.com",
        "feeds.feedburner.com",
        "feedproxy.google.com"
    ]

    start_urls = [
        "http://feeds.feedburner.com/EverydayFoodBlog",
        "http://feeds.feedburner.com/ourfinds",
    ]

    def parse(self, response):
      xxs = XmlXPathSelector(response)
      hxs = HtmlXPathSelector(response)
      links = xxs.select('//link/text()').extract()

      log.msg('Link length: %s' % len(links), level=log.ERROR)

      if len(links) <= 0:
        log.msg('no links found, using regular parser', level=log.ERROR)
        links = hxs.select('//a/@href').extract()

      msg = 'Links: %s' % links
      log.msg(msg, level=log.ERROR)

      return [Request(x, callback=self.parse_item) for x in links]
