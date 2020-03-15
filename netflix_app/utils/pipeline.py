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


def process_item(item):
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
