from unittest import TestCase, skip

import textapp.text_app as ta


class TextMenuTest(TestCase):
    def test_main(self):
        self.assertEqual(ta.main(), ta.SUCCESS)

    def test_exec_choice(self):
        self.assertEqual(ta.exec_choice(ta.EXIT, ta.TEST_MENU), False)

    def test_is_valid_choice(self):
        self.assertTrue(ta.is_valid_choice(ta.CONTINUE, ta.TEST_MENU))
        self.assertTrue(ta.is_valid_choice(ta.EXIT, ta.TEST_MENU))
        self.assertFalse(ta.is_valid_choice(ta.BAD_CHOICE, ta.TEST_MENU))

    @skip("This test is stalling for input: must debug.")
    def test_run_form(self):
        self.assertIn(ta.TITLE, ta.run_form(ta.TEST_FORM))

    def test_menu_repr(self):
        self.assertIn(ta.MAIN_MENU, ta.menu_repr(ta.TEST_MENU))

    def test_data_repr(self):
        self.assertIn(ta.DATA_SET, ta.data_repr(ta.TEST_DATA)[ta.DATA_TEXT])
