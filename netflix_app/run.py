import crochet

from utils.data import get_new_content
from mail import send_email

crochet.setup()  # initialize crochet

from flask import Flask, render_template
from scrapy.crawler import CrawlerRunner
from ratings.ratings import NewContent, ComingSoon
from utils.rendering import render_template as render_mail

app = Flask('Netflix app', template_folder='netflix_app/templates')
crawl_runner = CrawlerRunner()  # requires the Twisted reactor to run

new_content_data = []
coming_soon_data = []

scrape_in_progress = False
scrape_complete = False


# new content
@app.route('/crawl/new_content')
def crawl_new_content():
    """
    Scrape for quotes
    """
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global new_content_data
        new_content_data = [] if new_content_data else new_content_data
        # start the crawler and execute a callback when complete
        scrape_with_crochet(NewContent, new_content_data)
        return 'SCRAPING'
    elif scrape_complete:
        scrape_complete = False
        scrape_in_progress = False
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'


@app.route('/results/new_content')
def get_results_new_content():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    if scrape_complete:
        try:
            data = get_new_content(new_content_data.copy())
        except AttributeError:
            data = new_content_data.copy()

        return render_template('new_content.html', data=data)
    return 'Scrape Still Progress'


@app.route('/send_mail/new_content')
def send_mail_new_content():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    global scrape_in_progress
    if scrape_complete:
        try:
            data = get_new_content(new_content_data.copy())
        except AttributeError:
            data = new_content_data.copy()
        send_email('New Content', render_mail('new_content.html', data=data))
        scrape_in_progress = False
        scrape_complete = False
        return render_template('email.html', command='New Content')
    return 'Scrape Still Progress'


# Coming Soon

@app.route('/crawl/coming_soon')
def crawl_coming_soon():
    """
    Scrape for quotes
    """
    global scrape_in_progress
    global scrape_complete

    if not scrape_in_progress:
        scrape_in_progress = True
        global coming_soon_data
        coming_soon_data = [] if coming_soon_data else coming_soon_data
        # start the crawler and execute a callback when complete
        scrape_with_crochet(ComingSoon, coming_soon_data)
        return 'SCRAPING'
    elif scrape_complete:
        scrape_complete = False
        scrape_in_progress = False
        return 'SCRAPE COMPLETE'
    return 'SCRAPE IN PROGRESS'


@app.route('/results/coming_soon')
def get_results_coming_soon():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    if scrape_complete:
        data = coming_soon_data.copy()
        return render_template('coming_soon.html', data=data[0])
    return 'Scrape Still Progress'


@app.route('/send_mail/coming_soon')
def send_mail_coming_soon():
    """
    Get the results only if a spider has results
    """
    global scrape_complete
    global scrape_in_progress
    if scrape_complete:
        data = coming_soon_data.copy()
        send_email('Coming Soon', render_mail('coming_soon.html', data=data[0]))
        scrape_in_progress = False
        scrape_complete = False
        return render_template('email.html', command='Coming Soon')
    return 'Scrape Still Progress'


@crochet.run_in_reactor
def scrape_with_crochet(spider, _data):
    eventual = crawl_runner.crawl(spider, content_data=_data)
    eventual.addCallback(finished_scrape)


def finished_scrape(null):
    """
    A callback that is fired after the scrape has completed.
    Set a flag to allow display the results from /results
    """
    global scrape_complete
    scrape_complete = True


if __name__ == '__main__':
    app.run()
