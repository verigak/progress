import unittest
from unittest.mock import patch

from progress import Infinite, Progress
from progress.bar import Bar
from progress.spinner import Spinner


class DurationTests(unittest.TestCase):
    def test_duration_retains_fractional_seconds_after_finish(self):
        for indicator_type in (Infinite, Progress, Bar, Spinner):
            with self.subTest(indicator=indicator_type):
                with patch('progress.monotonic', return_value=10.0) as clock:
                    indicator = indicator_type(file=None)
                    self.assertEqual(indicator.duration, 0.0)
                    clock.return_value = 10.25
                    self.assertEqual(indicator.duration, 0.25)
                    self.assertEqual(indicator.elapsed, 0)
                    indicator.finish()
                    clock.return_value = 20.0
                    self.assertEqual(indicator.duration, 0.25)
                    indicator.finish()
                    self.assertEqual(indicator.duration, 0.25)

    def test_context_manager_records_duration_on_exception(self):
        with patch('progress.monotonic', return_value=10.0) as clock:
            indicator = Bar(file=None)
            with self.assertRaises(ValueError):
                with indicator:
                    clock.return_value = 11.75
                    raise ValueError('work failed')
            clock.return_value = 30.0
            self.assertEqual(indicator.duration, 1.75)

    def test_finish_at_zero_timestamp_is_retained(self):
        with patch('progress.monotonic', return_value=0.0) as clock:
            indicator = Infinite(file=None)
            indicator.finish()
            clock.return_value = 2.0
            self.assertEqual(indicator.duration, 0.0)
