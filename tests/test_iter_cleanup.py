import gc
import unittest
import weakref

from progress import Infinite, Progress


class Payload(object):
    pass


class IterCleanupTest(unittest.TestCase):
    def test_close_releases_the_last_yielded_value(self):
        for cls in (Infinite, Progress):
            with self.subTest(cls=cls):
                indicator = cls(file=None)
                value = Payload()
                reference = weakref.ref(value)
                iterator = indicator.iter([value])
                next(iterator)
                del value
                iterator.close()
                gc.collect()
                self.assertIsNone(reference())
                self.assertFalse(hasattr(indicator, 'iter_value'))
                self.assertEqual(indicator.index, 0)

    def test_source_failure_releases_the_last_value(self):
        def broken_source():
            yield Payload()
            raise RuntimeError('source failed')

        for cls in (Infinite, Progress):
            with self.subTest(cls=cls):
                indicator = cls(file=None)
                iterator = indicator.iter(broken_source())
                value = next(iterator)
                reference = weakref.ref(value)
                del value
                with self.assertRaisesRegex(RuntimeError, 'source failed'):
                    next(iterator)
                gc.collect()
                self.assertIsNone(reference())
                self.assertFalse(hasattr(indicator, 'iter_value'))
                self.assertEqual(indicator.index, 1)

    def test_normal_iteration_still_cleans_up(self):
        for cls in (Infinite, Progress):
            indicator = cls(file=None)
            self.assertEqual(list(indicator.iter([1, 2])), [1, 2])
            self.assertEqual(indicator.index, 2)
            self.assertFalse(hasattr(indicator, 'iter_value'))


if __name__ == '__main__':
    unittest.main()
