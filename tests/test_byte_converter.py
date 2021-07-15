from unittest import TestCase
from koshi8bit.auto_scale import AutoScale


class Test(TestCase):
    def test_auto_scale_size(self):
        self.assertEqual('99 B', AutoScale.byte(99))
        self.assertEqual('1.0 kB', AutoScale.byte(1000))
        self.assertEqual('335.5 MB', AutoScale.byte(335528668))
        self.assertEqual('266.5 MB', AutoScale.byte(266530933))
