IMDB_CSS = 'div.ratingValue strong span::text'
ROTTEN_TOMATO_CSS = '.mop-ratings-wrap__percentage::text'
ROTTEN_TOMATO_RE = r'(\d+)%'


def parse_imdb(response):
    result = response.css(IMDB_CSS).get()
    yield {'imdb_score': result}


def parse_rtn_tmt(response):
    result = response.css(ROTTEN_TOMATO_CSS).re(ROTTEN_TOMATO_RE)
    if not result:
        yield {}
    yield {
        'rotten_tomatoes':
            {
                'critic_score': result[0],
                'audience_score': result[1]
            }
    }


config = {
    'imdb': parse_imdb,
    'rottentomatoes': parse_rtn_tmt,
}
