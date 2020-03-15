from scrapy import Spider


class ComingSoon(Spider):
    name = "coming_soon"
    start_urls = ["https://www.whats-on-netflix.com/coming-soon/"]

    def parse(self, response):
        dates = response.css('li.date-header h4::text').getall()
        titles = [title.split('(')[0] for title in response.css('li.title h5::text').getall()]
        _data = {title: date for title, date in zip(titles, dates)}
        self.content_data.append(_data)

