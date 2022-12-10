# noinspection PyCompatibility
import configparser
import logging
import os


class Config:
    """
    Configuration Object
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        dir = os.getcwd()
        # If windows, use backslashes
        if os.name == 'nt':
            dir += "\\"
        else:
            dir += "/"
        try:
            self.config.read(dir + "config.ini")
        except FileNotFoundError:
            logging.critical("Unable to retrieve configuration... Exiting.")
            exit(1)

        log_level_info = {'logging.DEBUG': logging.DEBUG,
                          'logging.INFO': logging.INFO,
                          'logging.WARNING': logging.WARNING,
                          'logging.ERROR': logging.ERROR,
                          }
        try:
            self.loglevel = log_level_info.get(self.config['Logging']['level'], logging.INFO)
        except KeyError:
            logging.critical("Unable to retrieve logging level... Exiting.")
            exit(1)
        logging.basicConfig(level=self.loglevel)
        try:
            self.apiKey = self.config["OpenAI"]["apiKey"]
            self.model = self.config["OpenAI"]["model"]
            self.temp = self.config["OpenAI"]["temp"]
            self.maxTokens = self.config["OpenAI"]["maxTokens"]
            self.prompt = self.config["OpenAI"]["prompt"]
            self.iter = self.config["OpenAI"]["iterations"]
            self.dataset = dir + self.config["Data"]["dataset"]
            self.output = dir + self.config["Data"]["output"]
            self.project = self.config["GCP"]["project"]
            self.endpoint = self.config["GCP"]["endpoint-id"]
            self.location = self.config["GCP"]["location"]
        except KeyError:
            logging.critical("Unable to retrieve configuration... Exiting.")
            exit(1)
        logging.debug("Configuration set.")
