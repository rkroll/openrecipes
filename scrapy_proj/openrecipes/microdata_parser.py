from microdata import URI
import microdata
from scrapy import log
from scrapy.selector import HtmlXPathSelector
import urlparse

def extract_facebook_images(response):
  # try facebook images
  image_path = '//meta[@property="og:image"]/@content'
  hxs = HtmlXPathSelector(response)
  image_scopes = hxs.select(image_path)

  images = []
  for image in image_scopes:
    images.append(image.extract())

  if len(images) >= 1:
    return images.pop()
  else:
    return None

def is_absolute(url):
  return bool(urlparse.urlparse(str(url)).scheme)

def parse_recipes(response, data={}):
  recipes = []

  items = microdata.get_items(response.body)


  for item in items:
    #log.msg(item.json(), level=log.DEBUG)

    recipe = {}

    if item.itemtype == [URI("http://data-vocabulary.org/Recipe")]:
      recipe = handle_data_vocab(item, data)
    elif item.itemtype == [URI("http://schema.org/Recipe")]:
      recipe = handle_schema_org(item, data)
    else:
      log.msg('could not determine microdata type', level=log.ERROR)

    if 'image' in recipe:
      img = recipe['image']
      fb_image = extract_facebook_images(response)

      if type(img) is str or type(img) is unicode and img.startswith('//'):
        recipe['image'] = extract_facebook_images(response)
      elif type(img) is URI and img.string.startswith('//'):
        recipe['image'] = extract_facebook_images(response)

      # favor facebook image
      if img != fb_image and fb_image is not None:
        recipe['image'] = fb_image;

    recipe['source'] = data['source']
    recipes.append(recipe)

  return recipes


def handle_schema_org(microdata, d):
  recipe = {}

  recipe['name'] = microdata.name
  recipe['description'] = microdata.description

  if microdata.image is not None: recipe['image'] = microdata.image.string

  if microdata.url is not None and is_absolute(microdata.url): recipe['url'] = microdata.url
  if 'url' not in recipe: recipe['url'] = d['url']

  recipe['creator'] = microdata.creator
  recipe['ingredients'] = set(microdata.get_all('ingredients'))
  recipe['datePublished'] = microdata.datePublished
  recipe['dateCreated'] = microdata.dateCreated
  recipe['recipeYield'] = microdata.recipeYield
  recipe['cookTime'] = microdata.cookTime
  recipe['prepTime'] = microdata.prepTime
  recipe['totalTime'] = microdata.totalTime
  recipe['recipeCategory'] = set(microdata.get_all('recipeCategory'))
  recipe['recipeInstructions'] = microdata.recipeInstructions

  if microdata.aggregateRating is not None: recipe['aggregateRating'] = microdata.aggregateRating.ratingValue
  if microdata.nutrition is not None:
    recipe['calories'] = microdata.nutrition.calories
    recipe['carbohydrateContent'] = microdata.nutrition.carbohydrateContent
    recipe['cholesterolContent'] = microdata.nutrition.cholesterolContent
    recipe['fatContent'] = microdata.nutrition.fatContent
    recipe['fiberContent'] = microdata.nutrition.fiberContent
    recipe['proteinContent'] = microdata.nutrition.proteinContent
    recipe['saturatedFatContent'] = microdata.nutrition.saturatedFatContent
    recipe['servingSize'] = microdata.nutrition.servingSize
    recipe['sodiumContent'] = microdata.nutrition.sodiumContent
    recipe['sugarContent'] = microdata.nutrition.sugarContent
    recipe['transFatContent'] = microdata.nutrition.transFatContent
    recipe['unsaturatedFatContent'] = microdata.nutrition.unsaturatedFatContent

  return recipe

def handle_data_vocab(microdata, d):
  recipe = {}

  recipe['name'] = microdata.name
  recipe['description'] = microdata.summary
  recipe['image'] = microdata.photo
  recipe['creator'] = microdata.author

  if microdata.url is not None: recipe['url'] = microdata.url
  if microdata.url is None: recipe['url'] = d['url']

  microdata_ingredients = microdata.get_all('ingredient')

  ingredients = []

  for item in microdata_ingredients:
    if item is not None:
      parts = []
      if item.amount is not None: parts.append(item.amount)
      if item.name is not None: parts.append(item.name)
      ingredients.append(" ".join(parts))

  recipe['ingredients'] = ingredients
  recipe['datePublished'] = microdata.published
  recipe['dateCreated'] = microdata.dateCreated
  recipe['recipeYield'] = microdata.get('yield')
  recipe['cookTime'] = microdata.get('cookTime')
  recipe['prepTime'] = microdata.prepTime
  recipe['totalTime'] = microdata.totalTime
  recipe['recipeCategory'] = microdata.get_all('recipeType')

  recipe['recipeInstructions'] = microdata.instructions

  if microdata.aggregateRating is not None: recipe['aggregateRating'] = microdata.aggregateRating.ratingValue

  nutrition_item = microdata.get('nutrition')

  if nutrition_item is not None:
    recipe['calories'] = microdata.nutrition.calories
    recipe['carbohydrateContent'] = microdata.nutrition.carbohydrate
    recipe['cholesterolContent'] = microdata.nutrition.cholesterol
    recipe['fatContent'] = microdata.nutrition.fatContent
    recipe['fiberContent'] = nutrition_item.fiber
    recipe['proteinContent'] = microdata.nutrition.protein
    recipe['saturatedFatContent'] = microdata.nutrition.saturatedFat
    recipe['servingSize'] = microdata.nutrition.servingSize
    recipe['sodiumContent'] = microdata.nutrition.sodium
    recipe['sugarContent'] = microdata.nutrition.sugar
    recipe['transFatContent'] = microdata.nutrition.transFat
    recipe['unsaturatedFatContent'] = microdata.nutrition.unsaturatedFat

  return recipe