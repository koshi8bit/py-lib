from unittest import TestCase
from koshi8bit.google_sheets.google_sheets import GoogleSheets


class TestGoogleSheets(TestCase):
    def test_read(self):
        sheet_to_write = 'test-sheet!'
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        lines = gs.read(sheet_to_write+'B1:D1')
        self.assertEqual([['tst1', 'tst2', 'tst3']], lines)

    def test_write(self):
        sheet_to_write = 'test-sheet!'
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        data = [[1, 2, 3], [4, '5', 6]]
        res = gs.write(sheet_to_write + 'B2:D2', data)
        self.assertTrue(res)
