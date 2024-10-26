import configparser
from os import listdir
import yaml
import os.path
import logging
import sys




class Config:
    CONFIG = configparser.ConfigParser()
    # CONFIG.read("/config.ini")


class YAMLConfig:
    LOG = logging.getLogger(__name__)
    CONFIG = dict()
    LOG.error(os.getenv("ROLES_MOD"))
    # try:
    #     with open("/config.yaml") as config_file:
    #         CONFIG = yaml.safe_load(config_file)
    # except FileNotFoundError:
    #     LOG.error(listdir())
    #     LOG.error(
    #         "Failed to load YAML config. "
    #         "Please make sure you've used config_converter.py "
    #         "to convert your config file to the new format "
    #         "or filled in config.yaml."
    #     )

    #     sys.exit(-1)
