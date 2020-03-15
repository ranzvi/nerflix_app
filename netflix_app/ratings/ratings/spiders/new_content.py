from scrapy import Spider

from .utils.title import get_new_titles, get_title_data


class NewContent(Spider):
    name = "new_content"
    start_urls = ["https://www.whats-on-netflix.com/whats-new/"]

    def parse(self, response):
        titles = get_new_titles(response)
        for title in titles:
            yield get_title_data(title, self.content_data)

