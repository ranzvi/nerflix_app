import os

from netflix_app.netflixapp.settings import CRAWLER_PROCESS_SETTINGS, OUTPUT_FOLDER


def load_settings(spider_name):
    process_settings = CRAWLER_PROCESS_SETTINGS.copy()
    process_settings['FEED_URI'] = process_settings['FEED_URI'].format(spider=spider_name)
    return process_settings


def clean_output_dir(f_name=None):
    if f_name:
        try:
            os.remove(os.path.join(OUTPUT_FOLDER, f_name))
        except FileNotFoundError:
            pass
    else:
        for filename in os.listdir(OUTPUT_FOLDER):
            os.remove(os.path.join(OUTPUT_FOLDER, filename))
