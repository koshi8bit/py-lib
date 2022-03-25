from unittest import TestCase
from lib.koshi8bit.easy_living import Pandas
import pandas as pd


class Test(TestCase):
    def __init__(self, argv):
        super().__init__(argv)
        d = {
            "a": {
                "x": 1,
                "y": 2
            },
            "b": {
                "x": 3,
                "y": 4
            }
        }
        self.df = pd.DataFrame(d)
        # Pandas.print(self.df, "test")

    def test_pandas_is_null(self):
        pass

    def test_df_to_str(self):
        self.assertEqual(Pandas.df_to_str(self.df, "test"),
                         """

### test ###
   a  b
x  1  3
y  2  4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df, "test", indent=False),
                         """### test ###
   a  b
x  1  3
y  2  4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df),
                         """

   a  b
x  1  3
y  2  4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df, indent=False),
                         """   a  b
x  1  3
y  2  4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df, show_len=False, indent=False),
                         """   a  b
x  1  3
y  2  4""")
