from unittest import TestCase

from API.db import get_games


class DBTestCase(TestCase):
    def test_get_games(self):
        games = get_games()
        self.assertTrue(isinstance(games, dict))
        self.assertTrue(len(games) > 1)
