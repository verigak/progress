import io
import sys
import unittest
from unittest.mock import patch

from progress.bar import Bar


class OutputStreamTests(unittest.TestCase):
    def test_default_uses_stderr_replaced_after_import(self):
        stream = io.StringIO()
        with patch.object(sys, 'stderr', stream):
            with Bar('download', max=1, check_tty=False, hide_cursor=False) as bar:
                self.assertIs(bar.file, stream)
                bar.next()
        self.assertIn('download', stream.getvalue())

    def test_existing_bar_follows_replaced_stderr(self):
        original, replacement = io.StringIO(), io.StringIO()
        with patch.object(sys, 'stderr', original):
            bar = Bar(check_tty=False, hide_cursor=False)
            before = original.getvalue()
            with patch.object(sys, 'stderr', replacement):
                bar.writeln('redirected')
                bar.finish()
            self.assertEqual(original.getvalue(), before)
        self.assertIn('redirected', replacement.getvalue())

    def test_explicit_stream_and_none_are_preserved(self):
        explicit, replacement = io.StringIO(), io.StringIO()
        with patch.object(sys, 'stderr', replacement):
            bar = Bar(file=explicit, check_tty=False, hide_cursor=False)
            bar.writeln('explicit')
            bar.finish()
            bar.file = None
            bar.writeln('disabled')
            bar.finish()
            self.assertIsNone(bar.file)
        self.assertIn('explicit', explicit.getvalue())
        self.assertNotIn('disabled', explicit.getvalue())
        self.assertEqual(replacement.getvalue(), '')

    def test_subclasses_can_keep_a_class_default_stream(self):
        stream = io.StringIO()

        class CustomBar(Bar):
            file = stream

        with CustomBar(check_tty=False, hide_cursor=False) as bar:
            self.assertIs(bar.file, stream)
            bar.writeln('class default')
        self.assertIn('class default', stream.getvalue())
