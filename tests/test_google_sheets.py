from unittest import TestCase
from koshi8bit.log.google_sheets.google_sheets import GoogleSheets
from koshi8bit.easy_living import Format

sheet = 'test-sheet'


class TestGoogleSheets(TestCase):
    def test_read(self):
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        lines = gs.read(sheet, 'B1:D1')
        self.assertEqual([['append1', 'append2', 'append3']], lines)

    def test_read_cell(self):
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        cell = gs.read_cell(sheet, 'F1')
        self.assertEqual(cell, 'write1')

    def test_append(self):
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        data = [[1, 2, 3], [4, '5', 6]]
        res = gs.append(sheet, 'B3:B', data)
        self.assertTrue(res)

        data = [[0.1, 0.2, 0.3], [0.4, '0.5', 0.6]]
        res = gs.append(sheet, 'B5:B', data)
        self.assertTrue(res)

    def test_write(self):
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        n = Format.date_time_ui(True, False)
        data = [[10, n, 30], [40, '50', 60]]
        res = gs.write(sheet, 'F3:H', data)
        self.assertTrue(res)

        cell = gs.read_cell(sheet, 'G3')
        self.assertEqual(n, cell)

    def test_clear(self):
        gs = GoogleSheets('../private/creds.json',
                          '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8')

        res = gs.clear(sheet, 'J3:L')
        self.assertTrue(res)

        n = Format.date_time_ui(True, False)
        data = [[10, n, 30], [40, '50', 60]]
        res = gs.write(sheet, 'J3:L', data)
        self.assertTrue(res)
