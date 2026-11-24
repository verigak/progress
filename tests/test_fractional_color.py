from unittest import TestCase
from unittest.mock import patch

from progress.bar import IncrementalBar


class FractionalColorTests(TestCase):
    def render(self, index, color):
        bar = IncrementalBar(max=8, width=4, phases=(' ', '.', '#'),
                             color=color, file=None, suffix='',
                             bar_prefix='[', bar_suffix=']')
        with patch.object(bar, 'writeln') as write:
            bar.goto(index)
        return write.call_args[0][0]

    def test_first_fractional_segment_uses_the_selected_color(self):
        self.assertEqual(self.render(1, 'red'), '[\x1b[31m.\x1b[0m   ]')

    def test_full_and_fractional_segments_share_the_color(self):
        self.assertEqual(self.render(5, 'red'), '[\x1b[31m##.\x1b[0m ]')
        self.assertEqual(self.render(8, 'red'), '[\x1b[31m####\x1b[0m]')

    def test_uncolored_fractional_bars_keep_their_width(self):
        self.assertEqual(self.render(1, None), '[.   ]')
        self.assertEqual(self.render(5, None), '[##. ]')
