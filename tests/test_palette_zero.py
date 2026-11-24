import unittest

from progress.colors import color


class PaletteZeroTests(unittest.TestCase):
    def test_zero_is_a_valid_foreground_and_background_index(self):
        self.assertEqual(color('text', fg=0), '\x1b[38;5;0mtext\x1b[0m')
        self.assertEqual(color('text', bg=0), '\x1b[48;5;0mtext\x1b[0m')
        self.assertEqual(color('text', fg=0, bg=255, style='bold'),
                         '\x1b[38;5;0;48;5;255;1mtext\x1b[0m')

    def test_optional_colors_and_named_black_keep_their_behavior(self):
        self.assertEqual(color('text'), 'text')
        self.assertEqual(color('text', fg='', bg=''), 'text')
        self.assertEqual(color('text', fg='black'), '\x1b[30mtext\x1b[0m')
        for value in (-1, 256):
            with self.assertRaises(Exception):
                color('text', fg=value)
            with self.assertRaises(Exception):
                color('text', bg=value)
