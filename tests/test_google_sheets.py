from unittest import TestCase
from lib.koshi8bit.log.google_sheets.google_sheets import GoogleSheets
from lib.koshi8bit.easy_living import Format

sheet = 'test-sheet'


class TestGoogleSheets(TestCase):
    def test_connect_with_invalid_creds(self):
        with self.assertRaises(BaseException):
            gs = GoogleSheets('../testCreds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)
            cell = gs.read_cell('Лист11', 'A1')
            print(cell)

    def test_connect_with_invalid_id_sheet(self):
        with self.assertRaises(BaseException):
            gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZN', None)
            cell = gs.read_cell('Лист11', 'A1')
            print(cell)

    def test_throws_exception_when_read_range(self):
        gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)

        with self.assertRaises(BaseException):
            lines = gs.read('Лист11', 'A999:B1B1')
            print(lines)

    def test_throws_exception_read_range_with_invalid_list(self):
        gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)

        with self.assertRaises(BaseException):
            lines = gs.read('Лист', 'A1:D4')
            print(lines)

    def test_throws_exception_when_read_cell(self):
        gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)

        with self.assertRaises(BaseException):
            cell = gs.read_cell('Лист11', 'AA1')
            print(cell)

    def test_throws_exception_read_cell_with_invalid_list(self):
        gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)

        with self.assertRaises(BaseException):
            cell = gs.read_cell('Лист12', 'A1')
            print(cell)

    def test_throws_exception_when_write_cell(self):
        gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)

        with self.assertRaises(BaseException):
            data = [[1, '2', 3], [4, 's5', 6]]
            res = gs.write('Лист11', 'B1B1:D', data)

    def test_throws_exception_write_with_invalid_list(self):
        gs = GoogleSheets('../creds.json', '1kr1hAsjx2UGm9AgZRvWlkMHSiG_T4WxE0VozZNK9gtY', None)

        with self.assertRaises(BaseException):
            data = [[1, '2', 3], [4, 's5', 6]]
            res = gs.write('Лист113', 'B1:D', data)

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
