import os
import barbados.util
from barbados.printers import KitchenCardPrinter

TEMPLATE_PATH = './templates/menu'


class MenuPrinter:
    def __init__(self):
        pass

    @staticmethod
    def render(sections):

        kcp = KitchenCardPrinter()

        section_template_path = os.path.join(TEMPLATE_PATH, 'section.html')
        section_template = barbados.util.load_template_from_file(section_template_path)

        menu_template_path = os.path.join(TEMPLATE_PATH, 'menu.html')
        menu_template = barbados.util.load_template_from_file(menu_template_path)

        rendered_sections = []
        cards_per_row = 4

        for section in sections:
            rendered_cocktails = []
            for c in section['cocktails']:
                for i in range(0, c.spec_count):
                    rendered_cocktails.append(kcp.render(cocktail=c, specindex=i))

            section_content = section_template.render(section=section, rendered_cocktails=rendered_cocktails, cards_per_row=cards_per_row)
            rendered_sections.append(section_content)

        menu_content = menu_template.render(rendered_sections=rendered_sections)
        barbados.util.write_file('./output/kitchen.html', menu_content)