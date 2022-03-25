from unittest import TestCase

import numpy as np

from lib.koshi8bit.easy_living import Pandas
import pandas as pd


class Test(TestCase):
    def __init__(self, argv):
        super().__init__(argv)
        d = {
            "r1": {
                "c1": 1,
                "c2": 2
            },
            "r2": {
                "c1": 3,
                "c2": 4
            }
        }
        self.df = pd.DataFrame(d).transpose()
        # Pandas.print(self.df, "test")

    def test_pandas_is_null(self):
        self.df["c3"] = [None, np.nan]
        self.df.loc['r3'] = [4, 5, 6]
        self.df.loc['r4'] = [7, 8, "asd"]
        Pandas.print(self.df)

    def test_df_to_str(self):
        self.assertEqual(Pandas.df_to_str(self.df, "test"),
                         """

### test ###
    c1  c2
r1   1   2
r2   3   4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df, "test", indent=False),
                         """### test ###
    c1  c2
r1   1   2
r2   3   4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df),
                         """

    c1  c2
r1   1   2
r2   3   4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df, indent=False),
                         """    c1  c2
r1   1   2
r2   3   4
len=2""")

        self.assertEqual(Pandas.df_to_str(self.df, show_len=False, indent=False),
                         """    c1  c2
r1   1   2
r2   3   4""")
