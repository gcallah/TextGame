from unittest import TestCase

from formatting import sep, title, DEF_SEP_CHAR, DEF_SEP_LEN

class FmtTests(TestCase):
    def test_sep(self):
        self.assertIn(DEF_SEP_CHAR*DEF_SEP_LEN, sep())

    def test_title(self):
        test_title = "Well?"
        self.assertIn(test_title, title(test_title))
