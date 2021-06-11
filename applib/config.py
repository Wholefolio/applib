import json
import collections
from abc import ABCMeta, abstractmethod


class IConfig(object, metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def load_file(filename):
        pass


class Config(object):

    @staticmethod
    def factory(filetype):
        filetypes = {
            "json": JsonConfig,
            "ini": IniConfig,
            "yaml": YamlConfig
        }
        return filetypes[filetype]()


class JsonConfig(IConfig):

    @staticmethod
    def load_file(filename):
        with open(filename, 'r') as f:
            options = collections.defaultdict(lambda: None, json.load(f))
        return options


class IniConfig(IConfig):

    @staticmethod
    def load_file(filename):
        pass


class YamlConfig(IConfig):
    @staticmethod
    def load_file(filename):
        pass
