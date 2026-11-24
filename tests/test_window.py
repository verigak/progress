import unittest
from unittest.mock import patch

from progress import Infinite
from progress.bar import Bar


class MovingAverageWindowTest(unittest.TestCase):
    def test_constructor_window_controls_recent_samples(self):
        with patch('progress.monotonic', side_effect=[0, 2, 4, 6]):
            indicator = Bar(file=None, sma_window=2, max=10)
            for duration in (1, 3, 9):
                indicator.update_avg(1, duration)
        self.assertEqual(list(indicator._xput), [3, 9])
        self.assertEqual(indicator.avg, 6)
        self.assertEqual(indicator.eta, 60)

    def test_window_larger_than_default_keeps_requested_history(self):
        with patch('progress.monotonic', side_effect=range(0, 50, 2)):
            indicator = Infinite(file=None, sma_window=12)
            for duration in range(1, 14):
                indicator.update_avg(1, duration)
        self.assertEqual(list(indicator._xput), list(range(2, 14)))
        self.assertEqual(indicator.avg, 7.5)

    def test_default_and_subclass_windows_are_preserved(self):
        class SmallWindow(Infinite):
            sma_window = 3

        self.assertEqual(Infinite(file=None)._xput.maxlen, 10)
        self.assertEqual(SmallWindow(file=None)._xput.maxlen, 3)
        self.assertEqual(SmallWindow(file=None, sma_window=5)._xput.maxlen, 5)


if __name__ == '__main__':
    unittest.main()
