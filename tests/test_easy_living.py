import os.path
from datetime import datetime
from unittest import TestCase
import lib.koshi8bit.easy_living as el
from lib.koshi8bit.easy_living import Utils
from pathlib import Path


class TestFormat(TestCase):
    def test_utils_dir(self):
        root_path = r'F:\home\koshi8bit\temp\adgfdgf\1'
        extra_path = os.path.join(root_path, r'2\3\4')

        if el.Utils.dir_exist(root_path):
            el.Utils.dir_rm(root_path)
        self.assertFalse(el.Utils.dir_exist(root_path))
        self.assertFalse(el.Utils.dir_exist(extra_path))

        el.Utils.dir_create(extra_path)
        self.assertTrue(el.Utils.dir_exist(root_path))
        self.assertTrue(el.Utils.dir_exist(extra_path))

        el.Utils.dir_rm(root_path)
        self.assertFalse(el.Utils.dir_exist(root_path))
        self.assertFalse(el.Utils.dir_exist(extra_path))

    def test_utils_dict_append(self):
        d = {1: ["a", "b"], 2: ["c"]}
        Utils.dict_append(d, 1, "b", False)
        self.assertEqual({1: ["a", "b"], 2: ["c"]}, d)

        Utils.dict_append(d, 1, "b", True)
        self.assertEqual({1: ["a", "b", "b"], 2: ["c"]}, d)

        Utils.dict_append(d, 3, "d")
        self.assertEqual({1: ["a", "b", "b"], 2: ["c"], 3: ["d"]}, d)



    def test_format_date_time_file(self):
        dt = datetime(2021, 7, 14, 13, 20, 16)
        f = el.Format.date_time_file(False)
        self.assertEqual('2021-07-14--13-20-16', dt.strftime(f))

    def test_format_date_time_ui_with_ms(self):
        dt = datetime(2021, 7, 14, 13, 20, 16, 123456)
        f = el.Format.date_time_ui(False, True)
        self.assertEqual('2021-07-14@13:20:16.123456', dt.strftime(f))

    def test_format_date_time_ui_without_ms(self):
        dt = datetime(2021, 7, 14, 13, 20, 16, 123)
        f = el.Format.date_time_ui(False, False)
        self.assertEqual('2021-07-14@13:20:16', dt.strftime(f))

    def test_format_double(self):
        self.assertEqual('3.140', el.Format.double(3.14, 3))
        self.assertEqual('3.14', el.Format.double(3.14, 2))
        self.assertEqual('3.00', el.Format.double(3, 2))

    def test_format_double_scientific_notation(self):
        self.assertEqual('3.140E+00', el.Format.double(3.14, 3, True))
        self.assertEqual('3.140E-01', el.Format.double(0.314, 3, True))

    def test_format_double_separator_sign(self):
        self.assertEqual('0,314', el.Format.double(0.314, 3, separator_sign=','))
