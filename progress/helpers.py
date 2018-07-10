# Copyright (c) 2012 Giorgos Verigakis <verigak@gmail.com>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import print_function


HIDE_CURSOR = '\x1b[?25l'
SHOW_CURSOR = '\x1b[?25h'


class WriteMixin(object):
    check_tty = True
    hide_cursor = False

    def __init__(self, message=None, **kwargs):
        super(WriteMixin, self).__init__(**kwargs)
        self._width = 0
        if message:
            self.message = message

        if self.file and self.is_tty():
            if self.hide_cursor:
                print(HIDE_CURSOR, end='', file=self.file)
            print(self.message, end='', file=self.file)
            self.file.flush()

    def write(self, s):
        if self.file and self.is_tty():
            line = self.message + s.ljust(self._width)
            print('\r' + line, end='', file=self.file)
            self._width = max(self._width, len(s))
            self.file.flush()

    def finish(self):
        if self.file and self.is_tty() and self.hide_cursor:
            print(SHOW_CURSOR, end='', file=self.file)

    def is_tty(self):
        return self.file.isatty() if self.check_tty else True


class WritelnMixin(object):
    check_tty = True
    hide_cursor = False

    def __init__(self, message=None, **kwargs):
        super(WritelnMixin, self).__init__(**kwargs)
        if message:
            self.message = message

        if self.file and self.is_tty() and self.hide_cursor:
            print(HIDE_CURSOR, end='', file=self.file)

    def clearln(self):
        if self.file and self.is_tty():
            print('\r\x1b[K', end='', file=self.file)

    def writeln(self, line):
        if self.file and self.is_tty():
            self.clearln()
            print(line, end='', file=self.file)
            self.file.flush()

    def finish(self):
        if self.file and self.is_tty():
            print(file=self.file)
            if self.hide_cursor:
                print(SHOW_CURSOR, end='', file=self.file)

    def is_tty(self):
        return self.file.isatty() if self.check_tty else True


from signal import signal, SIGINT
from sys import exit


class SigIntMixin(object):
    """Registers a signal handler that calls finish on SIGINT"""

    def __init__(self, *args, **kwargs):
        super(SigIntMixin, self).__init__(*args, **kwargs)
        signal(SIGINT, self._sigint_handler)

    def _sigint_handler(self, signum, frame):
        self.finish()
        exit(0)
