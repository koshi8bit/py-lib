import time
from unittest import TestCase
from freezegun import freeze_time
import os

from koshi8bit.log.excel.excel import Excel
from datetime import datetime


class TestExcel(TestCase):
    def test_init(self):
        with freeze_time("2021-07-14 13:20:16.123456"):
            excel = Excel(r'C:\tmp', ['-'])
            self.assertEqual(r'C:\tmp\2021-07-14--13-20-16.xls', excel.file_name)
            excel.close()

    def test__format_data(self):
        excel = Excel(r'C:\tmp', ['one', 'two', 'three'])
        self.assertEqual(['1,030E+01', '1,600E+01', '3,000E-01'], excel._format_data([10.3, 16, 0.3]))
        excel.close()

    def test__prepare_line(self):
        excel = Excel(r'C:\tmp', ['one', 'two', 'three'])
        self.assertEqual('1\t33.6\ttwo\n', excel._prepare_line(['1', '33.6', 'two']))
        excel.close()

    def test_commit(self):
        with freeze_time("2021-07-14 13:20:16.123456"):
            excel = Excel(r'C:\tmp', ['one', 'two'])
            excel._bw_commit.stop()

        with freeze_time("2021-07-14 13:21:16.123456"):
            excel.commit([10.2, 16])
            excel.commit([11.3, 16.9])
            self.assertEqual([[10.2, 16], [11.3, 16.9]], excel._commit_buffer)
            # self.assertEqual(
            #     'time\tdatetime\tone\ttwo\n'
            #     '13:21:16\t2021-07-14@13:21:16.123456\t1,020E+01\t1,600E+01\n'
            #     '13:21:16\t2021-07-14@13:21:16.123456\t1,130E+01\t1,690E+01\n', excel._buffer)

            excel.close()

    def test__commit_n_records(self):
        with freeze_time("2021-07-14 13:20:16.123456"):
            excel = Excel(r'C:\tmp', ['one', 'two'])
            excel._bw_commit.stop()

        with freeze_time("2021-07-14 13:21:16.123456"):
            a = excel._calc_avg([10.2, 11.3])
            b = excel._calc_avg([16, 16.9])
            excel.commit([10.2, 16])
            excel.commit([11.3, 16.9])
            excel._commit_n_records()
            self.assertEqual(
                '13:21:16\t2021-07-14@13:21:16.123456\t1,075E+01\t1,645E+01\n', excel._buffer)

        excel.close()

    def test__prepare_n_records(self):
        with freeze_time("2021-07-14 13:20:16.123456"):
            excel = Excel(r'C:\tmp', ['one', 'two'])
            excel._bw_commit.stop()

        with freeze_time("2021-07-14 13:21:16.123456"):
            a = excel._calc_avg([10.2, 11.3])
            b = excel._calc_avg([16, 16.9])
            excel.commit([10.2, 16])
            excel.commit([11.3, 16.9])
            self.assertEqual([a, b], excel._prepare_n_records())

        excel.close()

    def test_push(self):
        try:
            os.remove(r'C:\tmp\2021-07-14--13-21-16.xls')
        except OSError:
            pass

        with freeze_time("2021-07-14 13:21:16.123456"):
            excel = Excel(r'C:\tmp', ['one', 'two'])
            excel._bw_commit.stop()
            excel.commit([10.2, 16])
            excel.commit([11.3, 16.9])
            excel._commit_n_records()
            excel.push()
            name = excel.file_name
            # del excel

            with open(name, 'r') as f:
                self.assertEqual(
                    'time\tdatetime\tone\ttwo\n'
                    '13:21:16\t2021-07-14@13:21:16.123456\t1,075E+01\t1,645E+01\n', f.read())

        # os.remove(r'C:\tmp\2021-07-14--13-21-16.xls')
        excel.close()
