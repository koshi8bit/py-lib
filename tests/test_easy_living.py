import json
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

    def test_somesss(self):
        original = {1: 'one', 2: 'two'}
        new = original.copy()
        original[3] = "three"

        print('Orignal: ', original)
        print('New: ', new)
        self.assertTrue(True)

    def test_utils_dict_append(self):
        d = {1: ["a", "b"], 2: ["c"]}
        d2 = Utils.dict_append(d, 1, "b", False)
        self.assertEqual(d, d2)

        d2 = Utils.dict_append(d, 1, "b", True)
        self.assertEqual({1: ["a", "b", "b"], 2: ["c"]}, d2)

        d2 = Utils.dict_append(d2, 3, "d")
        self.assertEqual({1: ["a", "b", "b"], 2: ["c"], 3: ["d"]}, d2)

        d = {
                "user1": [
                    "123",
                    "456"
                ]
            }

        d2 = Utils.dict_append(d, "user1", "789")
        self.assertEqual(
            {
                "user1": [
                    "123",
                    "456",
                    "789"
                ]
            }, d2)

        d2 = Utils.dict_append(d, "user2", "789")
        self.assertEqual(
            {
                "user1": [
                    "123",
                    "456"
                ],
                "user2": [
                    "789"
                ]
            }, d2)

    def test_utils_dict_extend(self):
        d = {1: ["a", "b"], 2: ["c"]}
        d2 = Utils.dict_extend(d, 1, ["b", "c"])
        self.assertEqual({1: ["a", "b", "c"], 2: ["c"]}, d2)

        d2 = Utils.dict_extend(d, 1, ["b", "c"], True)
        self.assertEqual({1: ["a", "b", "b", "c"], 2: ["c"]}, d2)

    def test_utils_start_thread_pool(self):
        v = [
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
            (6, 2),
            (3, 10)
        ]

        def f(a, b):
            import time
            print("!", a, b)
            time.sleep(1)
            return a + b

        r = Utils.start_thread_pool(f, v)
        for res in r:
            self.assertEqual(res[0][0] + res[0][1], res[1])

        # self.assertEqual(r, [((3, 2), 5, None), ((5, 2), 7, None), ((2, 2), 4, None),
        #                      ((3, 10), 13, None), ((6, 2), 8, None), ((4, 2), 6, None)])
        # print(r)

    def test_utils_start_thread_pool_class(self):
        class Data:
            def __init__(self):
                self.name = "faka"

            def f(self, comment: str, datas: list):
                import time
                print("starting", self.name, datas, f"add={comment}")
                time.sleep(1)
                print("stopping", self.name, datas, f"add={comment}")
                return datas[0] + datas[1]

            def do(self):
                data = [
                    ["1", [0, 1]],
                    ["5", [2, 3]]
                ]
                # data = list(map(lambda x: (self, x), data))
                # print(f"{data=}")

                res = Utils.start_thread_pool(self.f, data)
                # print(res)
                return res
                # print(json.dumps(dict(res), indent=4))

        d = Data()
        for r in d.do():
            print(r)
            self.assertEqual(r[0][1][0] + r[0][1][1], r[1])

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
        self.assertEqual('3.140', Format.double(3.14))

        self.assertEqual('3.14', Format.double(3.14, 2))
        self.assertEqual('3.1', Format.double(3.14, 1))
        self.assertEqual('3.00', Format.double(3, 2))

        self.assertEqual('3.140E+00', Format.double(3.14, 3, True))
        self.assertEqual('3.140E-01', Format.double(0.314, 3, True))

        self.assertEqual('0,314', Format.double(0.314, 3, comma_separator=','))

        self.assertEqual('12345.60', Format.double(12345.6, 2))
        self.assertEqual("12'345,60", Format.double(12345.6, 2,
                                                    comma_separator=",",
                                                    thousands_separator="'"))

        self.assertEqual("12'345.60", Format.double(12345.6, 2, thousands_separator="'"))

        self.assertEqual("1,23E+04", Format.double(12345.6, 2,
                                                   scientific_notation=True,
                                                   comma_separator=",",
                                                   thousands_separator="'"))
