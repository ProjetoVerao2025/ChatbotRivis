# This file loads the .env file and fills the config fields
from dataclasses import dataclass
from configparser import ConfigParser
import os


# Defining how our config should be, with all the fields, their types and default values.
@dataclass
class Config:
    week_meals_file: str = 'weekly-data.json'
    config_file: str = 'config.ini'
    url_cardapio: str = 'https://sistemas.prefeitura.unicamp.br/apps/cardapio/index.php'

    def load(self):
        config = ConfigParser()
        if not os.path.exists(self.config_file):
            self.save()
            return

        config.read(self.config_file)
            

        if "config" in config:
            c = config["config"]
            data.url_cardapio = c.get("url_cardapio", data.url_cardapio)
            data.week_meals_file = c.get("week_meals_file", week_meals_file)
        return

    def save(self):
        config = ConfigParser()
        config["config"] = {
                "url_cardapio": self.url_cardapio,
                "week_meals_file": self.week_meals_file,
                "config_file": self.config_file,
                }
        with open(self.config_file, "w") as file:
            config.write(file)



# Loading the config and making it acessible as variable
config = Config()
config.load()
