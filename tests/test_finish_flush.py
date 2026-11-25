import io
import unittest

from progress import Infinite, SHOW_CURSOR


class FinishFlushTest(unittest.TestCase):
    def test_finish_flushes_cursor_restoration(self):
        output = io.BytesIO()
        stream = io.TextIOWrapper(output, encoding='utf-8')
        indicator = Infinite(file=stream, check_tty=False)

        indicator.finish()

        self.assertTrue(output.getvalue().endswith(SHOW_CURSOR.encode('utf-8')))

    def test_finish_flushes_newline_without_hiding_cursor(self):
        output = io.BytesIO()
        stream = io.TextIOWrapper(output, encoding='utf-8')
        indicator = Infinite(file=stream, check_tty=False, hide_cursor=False)

        indicator.finish()

        self.assertTrue(output.getvalue().endswith(b'\n'))

    def test_context_manager_flushes_when_work_raises(self):
        output = io.BytesIO()
        stream = io.TextIOWrapper(output, encoding='utf-8')

        with self.assertRaises(ValueError):
            with Infinite(file=stream, check_tty=False):
                raise ValueError('work failed')

        self.assertTrue(output.getvalue().endswith(SHOW_CURSOR.encode('utf-8')))


if __name__ == '__main__':
    unittest.main()
