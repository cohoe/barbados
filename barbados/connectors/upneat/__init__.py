import requests
import json
import yaml
import string
import re
import logging
from slugify import slugify
from barbados.connectors.upneat.recipe import UpneatRecipeParser
from bs4 import BeautifulSoup

url_base = 'http://www.upneat.rocks'

endpoints = {
    'categories': 'ingredient/categories',
    'families': 'ingredient/categories/%i/families',
    'ingredients': 'ingredient/families/%i/ingredient_tree',
    'recipe': 'recipes/%s',
    'recipe_alpha': 'recipes/alpha_recipes?letter=%s',
}


class UpneatConnector:
    def __init__(self):
        pass

    @staticmethod
    def scrape_ingredients():

        scrape_dicts = []
        returns = []

        categories = UpneatConnector._get_categories()

        for category in categories:
            scrape_dicts.append(category)
            families = UpneatConnector._get_families(category)

            for family in families:
                scrape_dicts.append(family)
                ingredients = UpneatConnector._get_ingredients(family)

                for ingredients in ingredients:
                    scrape_dicts.append(ingredients)

            # break

        for scrape_dict in scrape_dicts:
            returns.append({
                'slug': scrape_dict['slug'],
                'display_name': scrape_dict['text'],
                'parent': scrape_dict['parent'],
                'type': scrape_dict['type']
            })

        print(yaml.dump(returns))

    @staticmethod
    def _get_ingredients(family):
        raw_ingredients = json.loads(requests.get("%s/%s" % (url_base, endpoints['ingredients'] % family['id'])).text)

        ing_dicts = []
        for top_ingredient in raw_ingredients:
            top_ingredient['parent'] = slugify(family['text'])
            top_ingredient['type'] = 'ingredient'
            top_ingredient['slug'] = slugify(top_ingredient['text'])
            children = top_ingredient.pop('children')
            top_ingredient.pop('a_attr')
            ing_dicts.append(top_ingredient)

            for sub_ingredient in children:
                sub_ingredient['type'] = 'ingredient'
                sub_ingredient['parent'] = slugify(top_ingredient['text'])
                sub_ingredient['slug'] = slugify(sub_ingredient['text'])
                sub_ingredient.pop('a_attr')
                ing_dicts.append(sub_ingredient)

        return ing_dicts

    @staticmethod
    def _get_families(category):
        raw_fams = json.loads(requests.get("%s/%s" % (url_base, endpoints['families'] % category['id'])).text)

        fam_dicts = []
        for family in raw_fams:
            family['id'] = int(family['id'].replace('family_', ''))
            family['type'] = 'family'
            family['parent'] = slugify(category['text'])
            family['slug'] = slugify(family['text'])
            fam_dicts.append(family)

        return fam_dicts

    @staticmethod
    def _get_categories():
        raw_cats = json.loads(requests.get("%s/%s" % (url_base, endpoints['categories'])).text)

        cat_dicts = []
        for category in raw_cats:
            category['id'] = int(category['id'].replace('category_', ''))
            category['type'] = 'category'
            category['parent'] = None
            category['slug'] = slugify(category['text'])
            cat_dicts.append(category)

        return cat_dicts

    @staticmethod
    def scrape_recipe(recipe):
        url = "%s/%s" % (url_base, endpoints.get('recipe') % recipe)
        logging.info("scraping %s" % url)
        parser = UpneatRecipeParser(slug=recipe, url=url)
        raw_recipe = parser.parse()

        return raw_recipe

    @staticmethod
    def get_recipes():
        # character_list = list(range(0, 10)) + list(string.ascii_uppercase)
        character_list = [1, 'A']

        raw_recipes = []

        for char in character_list:
            # print(UpneatConnector._get_recipes_alpha(char))
            slugs = UpneatConnector._get_recipes_alpha(char)
            for slug in slugs:
                raw_recipes.append(UpneatConnector.scrape_recipe(slug))

        return raw_recipes

    @staticmethod
    def _get_recipes_alpha(char):
        baseurl = "%s/%s" % (url_base, endpoints.get('recipe_alpha') % char)

        headers = {
            'X-Requested-With': 'XMLHttpRequest'
        }

        content = requests.get(baseurl, headers=headers).content.decode('UTF-8')

        # Cleanup
        content = content.replace("$('#alpha_recipes_partial').html(\"", '')
        content = content.replace("\");", '')
        content = BeautifulSoup(content, features='html.parser')

        recipes = []
        links = content.find_all('a')
        for link in links:
            slug = link.attrs.get('href')
            # slug = re.sub(r"[\"]+]", r'', slug)
            slug = slug.replace('\\"/recipes/', '')
            slug = slug.replace('\\"', '')
            recipes.append(slug)

        return recipes
        # return content