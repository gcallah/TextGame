import os

import textgame.text_game as tg


def test_main_bad_url():
    os.environ[tg.API_SERVER_URL] = 'http://not.good.url'
    assert tg.main() == tg.ERROR
