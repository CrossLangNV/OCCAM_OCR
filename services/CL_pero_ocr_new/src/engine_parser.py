import configparser
import os


def get_config(config_path):
    assert os.path.exists(config_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
