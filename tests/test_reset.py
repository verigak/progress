from io import StringIO
import unittest
from unittest.mock import patch

from progress import HIDE_CURSOR, SHOW_CURSOR
from progress.bar import Bar
from progress.spinner import Spinner


class ResetTests(unittest.TestCase):
    def test_reuse_iterator(self):
        bar = Bar('Files', file=None)
        self.assertEqual(list(bar.iter([1, 2, 3])), [1, 2, 3])
        bar.reset()
        self.assertEqual(bar.index, 0)
        self.assertEqual(list(bar.iter([4, 5])), [4, 5])
        self.assertEqual(bar.index, 2)
        self.assertEqual(bar.max, 2)
        self.assertEqual(bar.percent, 100)

    def test_reset_timing_and_average(self):
        with patch('progress.monotonic', return_value=10) as clock:
            bar = Bar(file=None, max=4)
            clock.return_value = 14
            bar.next(2)
            self.assertEqual(bar.avg, 2)
            self.assertEqual(bar.eta, 4)
            clock.return_value = 100
            bar.reset()
            self.assertEqual(bar.elapsed, 0)
            self.assertEqual(bar.avg, 0)
            self.assertEqual(bar.eta, 0)
            self.assertEqual(bar.remaining, 4)
            clock.return_value = 101
            bar.next()
            self.assertEqual(bar.elapsed, 1)
            self.assertEqual(bar.avg, 1)
            self.assertEqual(bar.eta, 3)

    def test_configuration_is_preserved(self):
        output = StringIO()
        bar = Bar('Custom', file=output, max=7, width=5,
                  suffix='%(index)d of %(max)d', hide_cursor=False,
                  check_tty=False)
        bar.next(7)
        bar.finish()
        bar.reset()
        self.assertIs(bar.file, output)
        self.assertEqual(bar.message, 'Custom')
        self.assertEqual(bar.max, 7)
        self.assertEqual(bar.width, 5)
        self.assertTrue(output.getvalue().endswith('\rCustom |     | 0 of 7'))
        bar.finish()

    def test_reset_spinner(self):
        spinner = Spinner(file=None)
        spinner.next(5)
        spinner.reset()
        self.assertEqual(spinner.index, 0)
        self.assertEqual(list(spinner.iter([1, 2])), [1, 2])
        self.assertEqual(spinner.index, 2)

    def test_cursor_is_hidden_again_after_finish(self):
        output = StringIO()
        bar = Bar(file=output, check_tty=False)
        bar.next()
        bar.finish()
        bar.reset()
        bar.next()
        bar.finish()
        self.assertEqual(output.getvalue().count(HIDE_CURSOR), 2)
        self.assertEqual(output.getvalue().count(SHOW_CURSOR), 2)

    def test_reset_does_not_hide_cursor_twice(self):
        output = StringIO()
        bar = Bar(file=output, check_tty=False)
        bar.reset()
        bar.finish()
        self.assertEqual(output.getvalue().count(HIDE_CURSOR), 1)
        self.assertEqual(output.getvalue().count(SHOW_CURSOR), 1)
