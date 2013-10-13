from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from openrecipes.items import RecipeItem, RecipeItemLoader
from openrecipes.util import flatten


class TasteofhomeMixin(object):
  source = 'tasteofhome'

  def _parse(self, root, schema, data={}):
    rootStr = root.extract()
    attrMap = {
      'photo': '@src',
      'image': '@src',
      'url': '@href',
      'prepTime': '@content',
      'cookTime': '@content',
      'totalTime': '@content',
      'datePublished': '@content',
      }
    data['itemtype'] = schema
    props = root.select('.//*[@itemprop]')

    for prop in props:
      node = prop
      skip = False
      name = prop.select('@itemprop').extract()[0]
      prevValue = data.get(name, None)

      while True:
        if node.extract() == rootStr:
          break
        if node.select('@itemscope'):
          skip = True
          break

        node = node.select('parent::*')[0]

      if skip:
        continue

      if prop.select('@itemscope'):
        value = _parse(prop, prop.select('@itemtype').extract()[0])
      else:
        value = [''.join(prop.select(attrMap.get(name, ".//text()[normalize-space()]")).extract()).strip()]

      if prevValue is None:
        data[name] = value
      else:
        prevValue.extend(value)

    return data


  def parse_recipes(self, scope, data={}):
    schema = 'http://schema.org/recipe'
    recipes = [self._parse(recipe, schema, data) for recipe in scope.select('//*[@itemtype="%s"]' % schema)]

    return recipes

  def parse_item(self, response):
    hxs = HtmlXPathSelector(response)
    raw_recipes = self.parse_recipes(hxs, {'source': self.source, 'url': response.url})
    for recipe in raw_recipes:
      if 'photo' in recipe:
        recipe['photo'] = flatten(recipe['photo'])
      if 'image' in recipe:
        recipe['image'] = flatten(recipe['image'])

    return [RecipeItem.from_dict(recipe) for recipe in raw_recipes]


class TasteofhomecrawlSpider(CrawlSpider, TasteofhomeMixin):

  name = "tasteofhome.com"

  allowed_domains = ["www.tasteofhome.com"]

  start_urls = [
    'http://www.tasteofhome.com/recipes/',
    ]

  rules = (
    # crawl all the cuisine pages, but dont try to parse
    Rule(SgmlLinkExtractor(allow=('/recipes/cuisine/.+'))),
    Rule(SgmlLinkExtractor(allow=('/recipes/ingredients/.+'))),
    Rule(SgmlLinkExtractor(allow=('/recipes/course/.+'))),
    Rule(SgmlLinkExtractor(allow=('/recipes/cooking-style/.+'))),
    Rule(SgmlLinkExtractor(allow=('/recipes/partner-recipes/.+'))),
    Rule(SgmlLinkExtractor(allow=('/recipes/.+')), callback='parse_item'),
    #Rule(SgmlLinkExtractor(allow=('\/recipes\/[a-zA-Z-/]+')), callback='parse_item'),
  )
