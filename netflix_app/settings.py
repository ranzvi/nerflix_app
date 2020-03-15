import yaml

CRAWLER_PROCESS_SETTINGS = {
    "FEED_FORMAT": "json",
    "FEED_URI": "../output/{spider}.json",
    "LOG_ENABLED": "False",
}
OUTPUT_FOLDER = '../output'
SCRAPY_SETTINGS_PATH = 'netflix_app.ratings.ratings.settings'
TEMPLATE_FOLDER = 'netflix_app/templates'

with open('netflix_app/config.yaml') as yml:
    CONFIG = yaml.safe_load(yml)
