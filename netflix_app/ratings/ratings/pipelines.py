# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json


def _process_ratings(ratings):
    p_ratings = []
    for r in ratings:
        rating = r.strip(' ').strip('%').split('/')[0]
        if rating == '100':
            rating = 10
        elif float(rating) > 10:
            rating = float(f'{rating[0]}.{rating[1]}')
        else:
            rating = float(rating)
        p_ratings.append(rating)
    return p_ratings


class NewContentPipeline(object):
    def process_item(self, item, spider):
        try:
            item['name'] = item['name'].rstrip(' ')
            item['description'] = item['description'].rstrip(' ')
            item['ratings'] = _process_ratings(item['ratings'])

            item['season_or_year'] = item['season_or_year'].strip(' (').strip(')')
            item['genre'] = item['genre'].lower().strip(' ').split(',')
            item['cast'] = item['cast'].rstrip(' ').split(', ')
            item['runtime'] = item['runtime'].strip(' ')
            item['language'] = item['language'].lower().strip(' ').split(',')
            item['awards'] = item.get('awards', '').rstrip(r'.\t')
            item['director'] = item.get('director', '').split(', ')

            return item
        except KeyError:
            return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open(f'./output/{spider.name}.json', 'w')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(item)
        self.file.write(line + '\n,')
        return item
