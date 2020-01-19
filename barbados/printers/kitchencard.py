import os
import barbados.util

TEMPLATE_PATH = './templates/kitchencard'


class KitchenCardPrinter:
    def __init__(self):
        pass

    @staticmethod
    def render(cocktail, specindex=0):
        spec = cocktail.specs[specindex]

        sections = {
            'title': None,
            'origin': None,
            'spec': None,
            'build': None,
            'instructions': None,
            'notes': None,
            'citations': None
        }

        for section in sections.keys():
            template_path = os.path.join(TEMPLATE_PATH, "%s.html" % section)
            jt = barbados.util.load_template_from_file(template_path)
            sections[section] = jt.render(cocktail=cocktail, spec=spec)

        card_template_path = os.path.join(TEMPLATE_PATH, 'kitchencard.html')
        jt = barbados.util.load_template_from_file(card_template_path)

        return jt.render(**sections)
