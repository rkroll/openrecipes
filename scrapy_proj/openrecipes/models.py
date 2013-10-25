#! -*- coding: utf-8 -*-

"""
Database models - defines table for storing scraped data.
Direct run will create the table.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from datetime import datetime

import settings


DeclarativeBase = declarative_base()

def fromdict(self, values):
  """Merge in items in the values dict into our object if it's one of our columns

  """
  print values
  for c in self.__table__.columns:
    if c.name in values:
      setattr(self, c.name, values[c.name])
    # else:
    #   print '%s not found in %s' % (c.name, self.__table__)


DeclarativeBase.fromdict = fromdict

category_join_table = Table(
  "categorizations",
  DeclarativeBase.metadata,
  Column("category_id", Integer, ForeignKey("categories.id")),
  Column("recipe_id", Integer, ForeignKey("recipes.id")),
  )


def db_connect():
  """Performs database connection using database settings from settings.py.

  Returns sqlalchemy engine instance.

  """
  print settings.DATABASE

  return create_engine(URL(**settings.DATABASE), convert_unicode=True, encoding="utf8")

def create_recipes_table(engine):
  """"""
  DeclarativeBase.metadata.create_all(engine)

def _get_date():
  return datetime.now()

class Publishers(DeclarativeBase):
  __tablename__ = "publishers"
  id = Column(Integer, primary_key=True)
  name = Column('name', String(length=255), nullable=False)
  display_name = Column('display_name', String(length=255), nullable=False)
  url = Column('url', String(length=255), nullable=False)
  created_at = Column(DateTime, nullable=False, default=_get_date())
  updated_at = Column(DateTime, nullable=False, default=_get_date(), onupdate=_get_date())

class RecipeIngredients(DeclarativeBase):
  __tablename__ = "ingredients"
  id = Column(Integer, primary_key=True)
  ingredient = Column('name', String(length=255), nullable=True)
  recipe_id = Column(Integer, ForeignKey('recipes.id'))
  created_at = Column(DateTime, nullable=False, default=_get_date())
  updated_at = Column(DateTime, nullable=False, default=_get_date(), onupdate=_get_date())

class Recipes(DeclarativeBase):
  """Sqlalchemy recipes model"""
  __tablename__ = "recipes"

  id = Column(Integer, primary_key=True)

  source = Column('source', String(length=255), nullable=True)

  # Thing
  description = Column('description', String(length=255), nullable=True)
  image = Column('original_photo_url', String(length=255), nullable=True)  # URL
  name = Column('name', String(length=255), nullable=False)
  url = Column('original_url', String(length=255), nullable=False)  # URL

  # CreativeWork
  creator = Column('author', String(length=255), nullable=True)  # Organization or Person -- not sure yet how to handle
  dateCreated = Column('created_at', DateTime, nullable=True, default=_get_date())  # ISO 8601 Date -- the orig item, not our copy
  dateModified = Column('updated_at', DateTime, nullable=True, default=_get_date(), onupdate=_get_date())  # ISO 8601 Date -- the orig item, not our copy
  datePublished = Column('date_published', DateTime, nullable=True)  # ISO 8601 Date -- the orig item, not our copy
  keywords = Column('keywords', String(length=255), nullable=True)

  # Recipe
  cookingMethod = Column('cooking_method', String(length=255), nullable=True)
  cookTime = Column('cook_time', String(length=255), nullable=True)  # ISO 8601 Duration
  ingredients = relationship("RecipeIngredients", uselist=True, cascade="all, delete, delete-orphan")
  prepTime = Column('prep_time', String(length=255), nullable=True)    # ISO 8601 Duration
  recipeCuisine = Column('recipe_cuisine', String(length=255), nullable=True)
  recipeInstructions = Column('instructions', String(length=255), nullable=True)  # we don't currently populate this
  recipeYield = Column('recipe_yield', String(length=255), nullable=True)
  totalTime = Column('total_time', String(length=255), nullable=True)  # ISO 8601 Duration

  categories = relationship("Category",
                            secondary=category_join_table)

  publisher_id = Column(Integer, ForeignKey('publishers.id'))

  valid_recipe = Column('valid_recipe', Boolean, nullable=False, default=False)
  aggregateRating = Column('aggregate_rating', String(length=255), nullable=True)

  # Votes
  up_votes = Column('up_votes', Integer, nullable=False, default=0)
  down_votes = Column('down_votes', Integer, nullable=False, default=0)

  # Nutrition
  calories = Column('calories', String(length=255), nullable=True)  # Energy. E.g., "100 calories" http://schema.org/Energy
  carbohydrateContent = Column('carbs', String(length=255), nullable=True)  # Mass. E.g., "7 kg" http://schema.org/Mass
  cholesterolContent = Column('cholesterol', String(length=255), nullable=True)  # Mass
  fatContent = Column('fat', String(length=255), nullable=True)  # Mass
  fiberContent = Column('fiber', String(length=255), nullable=True)  # Mass
  proteinContent = Column('protein', String(length=255), nullable=True)  # Mass
  saturatedFatContent = Column('saturated_fat', String(length=255), nullable=True)  # Mass
  servingSize = Column('serving_size', String(length=255), nullable=True)  # Mass
  sodiumContent = Column('sodium', String(length=255), nullable=True)  # Mass
  sugarContent = Column('sugar', String(length=255), nullable=True)  # Mass
  transFatContent = Column('transfat', String(length=255), nullable=True)  # Mass
  unsaturatedFatContent = Column('unsaturated_fat', String(length=255), nullable=True)  # Mass

  # Social
  fb_likes = Column('fb_likes', Integer, nullable=False, default=0)
  fb_shares = Column('fb_shares', Integer, nullable=False, default=0)
  pins = Column('pins', Integer, nullable=False, default=0)
  tweets = Column('tweets', Integer, nullable=False, default=0)


class Category(DeclarativeBase):
  __tablename__ = "categories"
  id = Column(Integer, primary_key=True)
  name = Column('name', String(length=255), nullable=False)
  created_at = Column(DateTime, nullable=False, default=_get_date())
  updated_at = Column(DateTime, nullable=False, default=_get_date(), onupdate=_get_date())
