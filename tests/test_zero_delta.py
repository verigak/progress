import unittest
from unittest.mock import patch

from progress import Progress


class ZeroDeltaTests(unittest.TestCase):
    def test_repeated_absolute_position_keeps_time_until_next_advance(self):
        clock = [0.0]
        with patch('progress.monotonic', side_effect=lambda: clock[0]):
            progress = Progress(max=4, file=None)
            clock[0] = 2.0
            progress.goto(1)
            clock[0] = 5.0
            progress.goto(1)
            self.assertEqual(progress.index, 1)
            self.assertEqual(progress.avg, 2.0)
            clock[0] = 8.0
            progress.goto(2)
            self.assertEqual(progress.avg, 4.0)
            self.assertEqual(progress.eta, 8)

    def test_zero_increment_before_first_item_includes_all_elapsed_time(self):
        clock = [0.0]
        with patch('progress.monotonic', side_effect=lambda: clock[0]):
            progress = Progress(max=3, file=None)
            clock[0] = 2.0
            progress.next(0)
            clock[0] = 5.0
            progress.next()
            self.assertEqual(progress.avg, 5.0)
            self.assertEqual(progress.eta, 10)
