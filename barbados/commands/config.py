import argparse
import sys
from barbados.objects import Config as config


class Config:
    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        # zk = ZookeeperConnector()

        test_key_path = "/barbados/cache/redis/host"
        test_key_value = "127.0.0.1"

        try:
            print(config.get(test_key_path))
            print(config.get(test_key_path))
            print(config.get(test_key_path))
            print(config.get(test_key_path))
        except KeyError:
            print("KeyError")
        config.set(test_key_path, test_key_value)
        # print(zk.get(test_key_path))


    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Manage configuration',
                                         usage='drink config <action> [key] [value]')
        parser.add_argument('action', help='action to perform', choices=['dump', 'get', 'set'])
        # parser.add_argument('key', default=None, help='configuration key')
        # parser.add_argument('value', default=None, help='configuration value')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
