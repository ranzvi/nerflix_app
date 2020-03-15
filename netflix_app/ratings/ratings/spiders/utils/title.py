def get_new_titles(response):
    titles = response.css('.new-title')
    return titles


def _get_ratings(title):
    ratings = title.css('.new-title-ratings::text')
    return [selector.root for selector in ratings][1:]


def _get_title_name(title):
    return title.css('h5::text').get()


def _get_title_season_or_year(title):
    return title.css('h5 small::text').get()


def _get_title_description(title):
    return title.css('.title-description::text').get()


def _get_data_block_from_title(title):
    return title.css('.new-title-right')


def _get_title_metadata(title):
    raw_metadata = title.css('::text').getall()[7:]
    keys = [a.strip(': ') for a in raw_metadata[::2]]
    values = raw_metadata[1::2]
    return {k.lower(): v for k, v in zip(keys, values)}


def get_title_data(title_data, content_data):
    data_block = _get_data_block_from_title(title_data)

    d = {
        'name': _get_title_name(data_block),
        'season_or_year': _get_title_season_or_year(data_block),
        'description': _get_title_description(data_block),
        'ratings': _get_ratings(title_data),
        **_get_title_metadata(data_block)
    }
    content_data.append(d)
    return d
