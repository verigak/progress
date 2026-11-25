from io import StringIO
import unittest

from progress import Infinite, Progress
from progress.bar import Bar
from progress.counter import Countdown
from progress.spinner import Spinner


class SubclassDefaultsTest(unittest.TestCase):
    def test_documented_message_default_is_rendered(self):
        class FancyBar(Bar):
            message = 'Loading'
            fill = '*'
            suffix = '%(percent).1f%% - %(eta)ds'

        output = StringIO()
        with FancyBar(file=output, check_tty=False, hide_cursor=False) as bar:
            bar.next()
        self.assertEqual(bar.message, 'Loading')
        self.assertIn('Loading |', output.getvalue())

    def test_maximum_defaults_are_inherited(self):
        for base in (Progress, Bar, Countdown):
            with self.subTest(base=base):
                class Parent(base):
                    max = 12

                class Child(Parent):
                    pass

                bar = Child(file=None)
                bar.next(6)
                self.assertEqual(bar.max, 12)
                self.assertEqual(bar.remaining, 6)
                self.assertEqual(bar.percent, 50)

    def test_infinite_indicators_inherit_message_defaults(self):
        for base in (Infinite, Spinner):
            with self.subTest(base=base):
                class Indicator(base):
                    message = 'Waiting '

                self.assertEqual(Indicator(file=None).message, 'Waiting ')

    def test_explicit_arguments_override_subclass_defaults(self):
        class FancyBar(Bar):
            message = 'Loading'
            max = 12

        bar = FancyBar('Other', max=20, file=None)
        self.assertEqual(bar.message, 'Other')
        self.assertEqual(bar.max, 20)
        empty = FancyBar('', max=0, file=None)
        self.assertEqual(empty.message, '')
        self.assertEqual(empty.max, 0)

    def test_builtin_defaults_and_instance_overrides_are_preserved(self):
        self.assertEqual(Bar(file=None).message, '')
        self.assertEqual(Bar(file=None).max, 100)
        first, second = Bar(file=None), Bar(file=None)
        first.message = 'First'
        first.max = 5
        self.assertEqual(second.message, '')
        self.assertEqual(second.max, 100)


if __name__ == '__main__':
    unittest.main()
