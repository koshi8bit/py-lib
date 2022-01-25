import json
from unittest import TestCase
from lib.koshi8bit.log.google_sheets.google_sheets import GoogleSheets
from lib.koshi8bit.easy_living import Format


class TestGoogleSheets(TestCase):
    def __init__(self, argv):
        super().__init__(argv)
        self.spreadsheet_id = '1Q3b0RAk8qLK-7H8c45p9TTqRgMjKD0NIs91uY4FZsy8'
        self.url = f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}'
        self.cred_file_valid = '../private/creds.json'
        self.cred_file_invalid = '../private/invalid_creds.json'
        self.sheet = 'test-sheet'

    def test_url_valid(self):
        with GoogleSheets(self.cred_file_valid, self.url) as gs:
            lines = gs.read(self.sheet, 'B1:D1')
            self.assertEqual([['append1', 'append2', 'append3']], lines)

        with GoogleSheets(self.cred_file_valid, self.url+"/") as gs:
            lines = gs.read(self.sheet, 'B1:D1')
            self.assertEqual([['append1', 'append2', 'append3']], lines)

        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            lines = gs.read(self.sheet, 'B1:D1')
            self.assertEqual([['append1', 'append2', 'append3']], lines)

    def test_read(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            lines = gs.read(self.sheet, 'B1:D1')
            self.assertEqual([['append1', 'append2', 'append3']], lines)

    def test_read_cell(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            cell = gs.read_cell(self.sheet, 'F1')
            self.assertEqual(cell, 'write1')

            cell = gs.read_cell(self.sheet, 'A1')
            self.assertEqual(cell, None)

    def test_append(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            data = [[1, 2, 3], [4, '5', 6]]
            gs.append(self.sheet, 'B3:B', data)

            data = [[0.1, 0.2, 0.3], [0.4, '0.5', '0,6']]
            gs.append(self.sheet, 'B5:B', data)

    def test_write(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            n = Format.date_time_ui(True, False)
            data = [[10, n, 30.1], ['40.1', None, '60,1']]
            gs.write(self.sheet, 'F3:H', data)

            cell = gs.read_cell(self.sheet, 'G3')
            self.assertEqual(n, cell)

            cell = gs.read_cell(self.sheet, 'G4')
            self.assertEqual(None, cell)

    def test_clear(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            gs.clear(self.sheet, 'J3:L')

            n = Format.date_time_ui(True, False)
            data = [[10, n, 30], [40, '50', 60]]
            gs.write(self.sheet, 'J3:L', data)

#################################

    def test_connect_with_invalid_creds(self):
        with self.assertRaises(GoogleSheets.InvalidCred):
            with GoogleSheets(self.cred_file_invalid, self.spreadsheet_id) as gs:
                cell = gs.read_cell(self.sheet, 'A1')
                print(cell)

    def test_connect_with_invalid_id_sheet(self):
        with self.assertRaises(GoogleSheets.InvalidSpreadsheetURLorId):
            with GoogleSheets(self.cred_file_valid, self.spreadsheet_id + '3') as gs:
                cell = gs.read_cell(self.sheet, 'A1')
                print(cell)

    def test_read_invalid_range(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.read(self.sheet, 'A999:B1B1')
                print(lines)

            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.read(self.sheet, 'A1A:B2')
                print(lines)

            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.read(self.sheet+"1", 'A1:D4')
                print(lines)

    def test_read_cell_invalid_range(self):
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.read(self.sheet, 'A1A:B2')
                print(lines)

            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.read(self.sheet + "1", 'A1:D4')
                print(lines)

    def test_write_invalid_range(self):
        data = [[1, '2', 3], [4, 's5', 6]]
        with GoogleSheets(self.cred_file_valid, self.spreadsheet_id) as gs:
            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.write(self.sheet, 'A999:B1B1', data)
                print(lines)

            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.write(self.sheet, 'A1A:B2', data)
                print(lines)

            with self.assertRaises(GoogleSheets.InvalidRange):
                lines = gs.write(self.sheet + "1", 'A1:D4', data)
                print(lines)