from io import StringIO
import unittest

from progress import Infinite
from progress.colors import bold, color, red


class AnsiWidthTests(unittest.TestCase):
    def render_updates(self, *lines):
        output = StringIO()
        indicator = Infinite(file=output, check_tty=False, hide_cursor=False)
        output.seek(0)
        output.truncate()
        for line in lines:
            indicator.writeln(line)
        return output.getvalue()

    def test_removing_color_does_not_add_visible_padding(self):
        styled = red('ready')
        self.assertEqual(self.render_updates(styled, 'ready'),
                         '\r' + styled + '\rready')

    def test_adding_color_still_erases_the_previous_longer_message(self):
        styled = bold('ok')
        self.assertEqual(self.render_updates('working', styled),
                         '\rworking\r' + styled + ' ' * 5)

    def test_nested_and_palette_styles_do_not_change_the_visible_width(self):
        styled = bold(color('ready', fg=200, bg='blue'))
        self.assertEqual(self.render_updates(styled, 'ok'),
                         '\r' + styled + '\rok   ')

    def test_plain_text_keeps_padding_to_the_longest_line(self):
        self.assertEqual(self.render_updates('working', 'ready', 'ok'),
                         '\rworking\rready  \rok     ')


if __name__ == '__main__':
    unittest.main()
