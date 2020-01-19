import yaml
import os


class Config:

    def __init__(self):
        self.config_file = self._find_config_file()

        with open(self.config_file, 'r') as fh:
            cfg = yaml.load(fh)

        for section in cfg:
            setattr(self, section, cfg[section])

    @staticmethod
    def _find_config_file():
        supported_paths = [
            'drink.yaml',
        ]
        for path in supported_paths:
            if os.path.exists(path):
                return path

        print("Could not find config file in any supported path. %s" % supported_paths)
        exit(1)


config = Config()