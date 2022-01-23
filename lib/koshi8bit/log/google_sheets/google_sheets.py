# https://habr.com/ru/post/483302/
import googleapiclient
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re
import validators


class GoogleSheets:
    service = None
    spreadsheet_id = None

    def __init__(self, creds_json: str, full_link: str):

        # self.check_cred_file(creds_json)
        self.credentials_file = creds_json
        try:
            self.connect()

        except FileNotFoundError as e:
            raise e

        except Exception:
            raise self.InvalidCred

        if validators.url(full_link):
            self.spreadsheet_id = self.parsing_id_from_table_link(full_link)
        elif full_link is None:
            raise ValueError("Id of the table is None. Perhaps you forgot to pass the required full_link parameter")
        else:
            self.spreadsheet_id = full_link

    class EmptyData(Exception):
        def __str__(self):
            return f"Data in this range is empty"

    class InvalidCred(Exception):
        def __str__(self):
            return "Credentials file is invalid"

    class InvalidSpreadsheetURLorId(Exception):
        def __str__(self):
            return "Spreadsheet URL or ID is invalid"

    class InvalidRange(Exception):
        def __init__(self, range_: str):
            self.range = range_

        def __str__(self):
            return f"Range is invalid ({self.range})"

    @staticmethod
    def check_cred_file(file_name: str):
        if not os.path.isfile(file_name):
            raise ValueError("Cred file does not exist")

    @staticmethod
    def parsing_id_from_table_link(full_link: str):
        sheet_id = re.search(r"https://docs\.google\.com/spreadsheets/d/(.+)/", full_link).group(1)
        if sheet_id is None:
            raise ValueError("Id sheets is None. Possible reasons for the error: an invalid URL was specified or "
                             "the file does not exist.")
        return sheet_id

    def connect(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        self.service = build('sheets', 'v4', http=http_auth)

    def disconnect(self):
        self.service.close()

    def _read(self, range_: str):
        try:
            result_input = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                    range=range_).execute()
            return result_input.get('values', [])

        except Exception as e:
            if 'Details: "Requested entity was not found."' in str(e):
                raise self.InvalidSpreadsheetURLorId
            if 'Details: "Unable to parse range: ' in str(e):
                raise self.InvalidRange(range_)
            raise e

    def read(self, sheet: str, pos: str):
        range_ = f'{sheet}!{pos}'
        return self._read(range_)

    def read_cell(self, sheet: str, pos: str):
        range_ = f'{sheet}!{pos}:{pos}'
        values_input = self._read(range_)

        if not values_input:
            raise self.EmptyData

        return values_input[0][0]

    def append(self, sheet: str, pos: str, data):
        rangee = f'{sheet}!{pos}'
        res = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=rangee, valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS", body={"values": data}
        ).execute()

        is_ok = isinstance(res, dict) and 'spreadsheetId' in res and res['spreadsheetId'] == self.spreadsheet_id

        if not is_ok:
            raise ValueError('error while writing to google sheet')

        return is_ok

    def write(self, sheet: str, pos: str, data):
        rangee = f'{sheet}!{pos}'
        res = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=rangee, valueInputOption="USER_ENTERED", body={"values": data}
        ).execute()

        is_ok = isinstance(res, dict) and 'spreadsheetId' in res and res['spreadsheetId'] == self.spreadsheet_id

        if not is_ok:
            raise ValueError('error while writing to google sheet')

        return is_ok

    def clear(self, sheet: str, pos: str):
        rangee = f'{sheet}!{pos}'
        body = {}
        res = self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id, range=rangee, body=body
        ).execute()

        is_ok = isinstance(res, dict) and 'spreadsheetId' in res and res['spreadsheetId'] == self.spreadsheet_id

        if not is_ok:
            raise ValueError('error while clearing to google sheet')

        return is_ok

    # def __del__(self):
    #     self.disconnect()
