from __future__ import unicode_literals

import unittest
from io import StringIO

from progress import SHOW_CURSOR
from progress.spinner import (Spinner, PieSpinner, MoonSpinner, LineSpinner,
                              PixelSpinner)


class SpinnerColorTests(unittest.TestCase):
    def make_spinner(self, spinner_type=Spinner, **kwargs):
        output = StringIO()
        spinner = spinner_type('Loading ', file=output, check_tty=False,
                               hide_cursor=False, **kwargs)
        output.seek(0)
        output.truncate()
        return spinner, output

    def test_color_wraps_only_phase(self):
        spinner, output = self.make_spinner(color='green')
        spinner.update()
        self.assertEqual(output.getvalue(), '\rLoading \x1b[32m-\x1b[0m')

    def test_default_output_stays_uncolored(self):
        spinner, output = self.make_spinner()
        spinner.next()
        self.assertEqual(output.getvalue(), '\rLoading \\')

    def test_explicit_none_stays_uncolored(self):
        spinner, output = self.make_spinner(color=None)
        spinner.update()
        self.assertEqual(output.getvalue(), '\rLoading -')

    def test_256_color_index(self):
        spinner, output = self.make_spinner(color=123)
        spinner.update()
        self.assertEqual(output.getvalue(), '\rLoading \x1b[38;5;123m-\x1b[0m')

    def test_all_spinner_phases_support_color(self):
        for spinner_type in (Spinner, PieSpinner, MoonSpinner, LineSpinner,
                             PixelSpinner):
            spinner, output = self.make_spinner(spinner_type, color='red')
            for index, phase in enumerate(spinner.phases):
                spinner.index = index
                output.seek(0)
                output.truncate()
                spinner.update()
                self.assertEqual(output.getvalue(),
                                 '\rLoading \x1b[31m' + phase + '\x1b[0m')

    def test_color_can_be_set_on_subclass(self):
        class RedSpinner(Spinner):
            color = 'red'
        spinner, output = self.make_spinner(RedSpinner)
        spinner.update()
        self.assertEqual(output.getvalue(), '\rLoading \x1b[31m-\x1b[0m')

    def test_colored_spinner_finishes_and_restores_cursor(self):
        output = StringIO()
        with Spinner('Loading ', color='green', file=output,
                     check_tty=False) as spinner:
            spinner.next()
        self.assertIn('\x1b[32m\\\x1b[0m', output.getvalue())
        self.assertTrue(output.getvalue().endswith('\n' + SHOW_CURSOR))
        self.assertFalse(spinner._hidden_cursor)


if __name__ == '__main__':
    unittest.main()
