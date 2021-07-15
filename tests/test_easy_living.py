from datetime import datetime
from unittest import TestCase
import koshi8bit.easy_living as el


class TestFormat(TestCase):
    def test_date_time_file(self):
        dt = datetime(2021, 7, 14, 13, 20, 16)
        f = el.Format.date_time_file()
        self.assertEqual('2021-07-14--13-20-16', dt.strftime(f))

    def test_date_time_ui_with_ms(self):
        dt = datetime(2021, 7, 14, 13, 20, 16, 123456)
        f = el.Format.date_time_ui(True)
        self.assertEqual('2021-07-14@13:20:16.123456', dt.strftime(f))

    def test_date_time_ui_without_ms(self):
        dt = datetime(2021, 7, 14, 13, 20, 16, 123)
        f = el.Format.date_time_ui(False)
        self.assertEqual('2021-07-14@13:20:16', dt.strftime(f))

    def test_double(self):
        self.assertEqual('3.140', el.Format.double(3.14, 3))
        self.assertEqual('3.14', el.Format.double(3.14, 2))
        self.assertEqual('3.00', el.Format.double(3, 2))

    def test_double_scientific_notation(self):
        self.assertEqual('3.140E+00', el.Format.double(3.14, 3, True))
        self.assertEqual('3.140E-01', el.Format.double(0.314, 3, True))

    def test_double_separator_sign(self):
        self.assertEqual('0,314', el.Format.double(0.314, 3, separator_sign=','))
