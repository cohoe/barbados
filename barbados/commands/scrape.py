import argparse
import sys
from barbados.connectors import UpneatConnector


class Scrape:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        cats = UpneatConnector.scrape_ingredients()
        # print(cats)


    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Scrape something',
                                         usage='drink scrape <source>')
        parser.add_argument('source', help='source')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
