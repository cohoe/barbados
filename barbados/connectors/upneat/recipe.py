import requests
import re
import logging
from bs4 import BeautifulSoup
from barbados.text import DisplayName, Slug
from barbados.factories import CocktailFactory


class UpneatRecipeParser:
    def __init__(self, slug, url):
        self.slug = slug
        self.url = url
        self.content = self._get_content(self.url)

    def parse(self):
        logging.info("Parsing slug %s" % self.slug)
        raw_recipe = self._content_to_dict()
        return CocktailFactory.raw_to_obj(raw_recipe=raw_recipe, slug=self.slug)

    def _get_content(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Bad get")

        full_content = BeautifulSoup(response.content, features="html.parser")
        return full_content.find_all('div', attrs={'class': 'container-fluid'})[1]

    def _content_to_dict(self):
        raw_dict = {
            'slug': self.slug,
            'display_name': self._get_display_name(),
            'specs': [{
                'slug': self._get_spec_slug(),
                'display_name': self._get_spec_display_name(),
                'origin': self._get_spec_origin(),
                'construction': self._get_construction(),
                'components': self._get_components(),
                'garnish': self._get_garnish(),
                'straw': self._get_straw(),
                'instructions': self._get_instructions(),
                'glassware': self._get_glassware(),
            }],
        }
        return raw_dict

    def _get_display_name(self):
        display_name = self.content.h3.next_element.strip()
        return DisplayName(display_name)

    def _get_spec_slug(self):
        slug = self.content.h3.p.a.text
        return Slug(slug)

    def _get_spec_display_name(self):
        name = self.content.h3.p.a.text
        # PDT doesn't work with DisplayName()
        return name

    def _get_spec_origin(self):
        story_element = self.content.find('p', attrs={'style': 'font-style:italic'})
        origin = {
            'story': story_element.text.strip().split(' —')[0] if story_element else None
        }
        return origin

    def _get_instructions(self):
        text = self.content.ul.find_next_sibling('p').text.strip()

        accepted_instructions = []
        for line in text.split('.')[:-1]:
            line = line.strip()
            if 'garnish' not in line.lower():
                accepted_instructions.append({'text': line})

        return accepted_instructions

    def _get_construction(self):
        instructions = self._get_instructions()
        search_string = instructions[0].get('text').lower()

        terms = ['shake', 'stir']
        for term in terms:
            if term in search_string:
                return term

        return 'unknown'

    def _get_components(self):
        raw_strings = [element.text.strip() for element in self.content.ul.find_all('li')]
        components = []

        for raw_string in raw_strings:
            if 'garnish' in raw_string.lower():
                continue

            if raw_string.startswith('dash'):
                raw_string = "1 %s" % raw_string

            tokens = re.split(r"([\.\d+]+) ([\w\.]+) (.*)$", raw_string)
            for token in tokens:
                if not token:
                    tokens.remove(token)

            try:
                component = {
                    'quantity': tokens[0],
                    'unit': tokens[1].replace('.', ''),
                    'name': tokens[2],
                }
            except IndexError:
                component = {
                    'name': tokens[0]
                }

            components.append(component)

        return components

    def _get_garnish(self):
        raw_strings = [element.text.strip() for element in self.content.ul.find_all('li')]
        garnishes = []

        for raw_string in raw_strings:
            if 'garnish' not in raw_string.lower():
                continue
            tokens = re.split(r"^(.*) \(Garnish\)$", raw_string)
            for token in tokens:
                if not token:
                    tokens.remove(token)

            garnish = {
                'slug': Slug(tokens[0])
            }

            garnishes.append(garnish)

        return garnishes

    def _get_straw(self):
        instructions = self._get_instructions()

        for instruction in instructions:
            if 'straw' in instruction.get('text').lower():
                return True

        return False

    def _get_glassware(self):
        instructions = self._get_instructions()

        for instruction in instructions:
            if 'glass' in instruction.get('text').lower():
                glass = re.sub(r"^(.*) (\w+) glass(.*)$", r'\2', instruction.get('text').lower())
                return [{'slug': Slug(glass)}]
