from settings import CONFIG
from .pipeline import process_item


def _parse_rating_setting(rating_setting):
    if not rating_setting:
        return lambda x: True
    if '+' in rating_setting and len(rating_setting) == 2:
        return lambda x: x >= float(rating_setting[0])
    if '-' in rating_setting and len(rating_setting) == 3 and rating_setting[1] == '-':
        return lambda x: float(rating_setting[0]) >= x >= float(rating_setting[2])


def _keep_result(result, genres, languages, rating_fn):
    if not set(genres).intersection(set(result['genre'])):
        return False

    if not set(languages).intersection(set(result['language'])):
        return False

    for rating in result['ratings']:
        if not rating_fn(rating):
            return False

    return True


def _parse_for_html(content):
    rating_sum = sum(content['ratings'])
    rating_len = len(content['ratings'])
    if rating_len == 0:
        content['ratings'] = 'No Ratings'
    else:
        content['ratings'] = "%.1f" % float(rating_sum / rating_len)
    content['genre'] = ', '.join(g.capitalize() for g in content['genre'])
    content['cast'] = ', '.join(content['cast'])
    content['director'] = ', '.join(content['director'])
    content['language'] = ', '.join(l.capitalize() for l in content['language'])
    return content


def get_new_content(new_content):
    processed_content = [process_item(c) for c in new_content]
    nc_config = CONFIG.get('new_content')
    genres = nc_config.get('genre')
    languages = nc_config.get('language')
    rating_fn = _parse_rating_setting(nc_config.get('ratings', None))

    kept_content = [_parse_for_html(c) for c in processed_content if _keep_result(c, genres, languages, rating_fn)]
    return kept_content
