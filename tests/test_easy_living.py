import os.path
from datetime import datetime
from unittest import TestCase
from lib.koshi8bit.easy_living import Utils, Format
from freezegun import freeze_time
from pathlib import Path


class TestFormat(TestCase):
    def test_utils_dir(self):
        root_path = r'F:\home\koshi8bit\temp\adgfdgf\1'
        extra_path = os.path.join(root_path, r'2\3\4')

        if Utils.dir_exist(root_path):
            Utils.dir_rm(root_path)
        self.assertFalse(Utils.dir_exist(root_path))
        self.assertFalse(Utils.dir_exist(extra_path))

        Utils.dir_create(extra_path)
        self.assertTrue(Utils.dir_exist(root_path))
        self.assertTrue(Utils.dir_exist(extra_path))

        Utils.dir_rm(root_path)
        self.assertFalse(Utils.dir_exist(root_path))
        self.assertFalse(Utils.dir_exist(extra_path))

    def test_utils_dict_append(self):
        d = {1: ["a", "b"], 2: ["c"]}
        Utils.dict_append(d, 1, "b", False)
        self.assertEqual({1: ["a", "b"], 2: ["c"]}, d)

        Utils.dict_append(d, 1, "b", True)
        self.assertEqual({1: ["a", "b", "b"], 2: ["c"]}, d)

        Utils.dict_append(d, 3, "d")
        self.assertEqual({1: ["a", "b", "b"], 2: ["c"], 3: ["d"]}, d)

    def test_format_date_time_file(self):
        dt = datetime(2021, 7, 14, 13, 20, 16, 123456)

        f = Format.date_time_file(dt, True)
        self.assertEqual('2021-07-14T13-20-16-123456', dt.strftime(f))

        f = Format.date_time_file(dt, False)
        self.assertEqual('2021-07-14T13-20-16', dt.strftime(f))

        f = Format.date_time_file(dt, False, Format.separator_file)
        self.assertEqual('2021-07-14--13-20-16', dt.strftime(f))

        self.assertEqual('%Y-%m-%d', Format.date_file_format)
        self.assertEqual('%H-%M-%S', Format.time_file_format)
        self.assertEqual('%H-%M-%S-%f', Format.time_file_ms_format)

        with freeze_time("2021-07-14 13:20:16.123456"):
            f = Format.date_time_file(None, False)
            self.assertEqual('2021-07-14T13-20-16', dt.strftime(f))

            f = Format.date_time_file(None, True)
            self.assertEqual('2021-07-14T13-20-16-123456', dt.strftime(f))

    def test_format_date_time_ui_with_ms(self):
        dt = datetime(2021, 7, 14, 13, 20, 16, 123456)

        f = Format.date_time_ui(dt, True)
        self.assertEqual('2021-07-14T13:20:16.123456', dt.strftime(f))

        f = Format.date_time_ui(dt, False)
        self.assertEqual('2021-07-14T13:20:16', dt.strftime(f))

        f = Format.date_time_ui(dt, False, Format.separator_ui)
        self.assertEqual('2021-07-14@13:20:16', dt.strftime(f))

        self.assertEqual('%Y-%m-%d', Format.date_ui_format)
        self.assertEqual('%H:%M:%S', Format.time_ui_format)
        self.assertEqual('%H:%M:%S.%f', Format.time_ui_ms_format)

        with freeze_time("2021-07-14 13:20:16.123456"):
            f = Format.date_time_ui(None, False)
            self.assertEqual('2021-07-14T13:20:16', dt.strftime(f))

            f = Format.date_time_ui(None, True)
            self.assertEqual('2021-07-14T13:20:16.123456', dt.strftime(f))

    def test_format_double(self):
        self.assertEqual('3.140', Format.double(3.14, 3))
        self.assertEqual('3.14', Format.double(3.14, 2))
        self.assertEqual('3.00', Format.double(3, 2))

    def test_format_double_scientific_notation(self):
        self.assertEqual('3.140E+00', Format.double(3.14, 3, True))
        self.assertEqual('3.140E-01', Format.double(0.314, 3, True))

    def test_format_double_separator_sign(self):
        self.assertEqual('0,314', Format.double(0.314, 3, separator_sign=','))
