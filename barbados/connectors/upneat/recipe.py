import requests
from bs4 import BeautifulSoup
from barbados.text import DisplayName, Slug


class UpneatRecipeParser:
    def __init__(self, slug, url):
        self.slug = slug
        self.url = url
        self.content = self._get_content(self.url)

    def parse(self):
        return self._content_to_dict()

    def _get_content(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Bad get")

        return BeautifulSoup(response.content, features="html.parser")

    def _content_to_dict(self):
        raw_dict = {
            'slug': self.slug,
            'display_name': self._get_display_name(),
            'specs': [{
                'slug': self._get_spec_slug(),
                'display_name': self._get_spec_display_name(),
                'origin': self._get_spec_origin(),
                'construction': None,
                'components': [],
                'garnish': [],
                'straw': None,
                'instructions': [self._get_instruction()]
            }],
        }
        return raw_dict

    def _get_display_name(self):
        display_name = self.content.find_all('div', attrs={'class': 'container-fluid'})[1].h3.contents[0]
        return DisplayName(display_name.strip())

    def _get_spec_slug(self):
        slug = self.content.find_all('div', attrs={'class': 'container-fluid'})[1].h3.p.a.text
        return Slug(slug)

    def _get_spec_display_name(self):
        name = self.content.find_all('div', attrs={'class': 'container-fluid'})[1].h3.p.a.text
        # PDT doesn't work with DisplayName()
        return name

    def _get_spec_origin(self):
        origin = {
            'story': self.content.find('p', attrs={'style': 'font-style:italic'}).text.strip().split(' —')[0]
        }
        return origin

    def _get_instruction(self):
        text = self.content.find_all('div', attrs={'class': 'container-fluid'})[1].ul
        return text