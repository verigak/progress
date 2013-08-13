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
    hide_cursor = False

    def __init__(self, message=None, **kwargs):
        super(WriteMixin, self).__init__(**kwargs)
        self._width = 0
        if message:
            self.message = message

        if self.file.isatty():
            if self.hide_cursor:
                print(HIDE_CURSOR, end='', file=self.file)
            print(self.message, end='', file=self.file)
            self.file.flush()

    def write(self, s):
        if self.file.isatty():
            b = '\b' * self._width
            c = s.encode('utf8').ljust(self._width)
            print(b + c, end='', file=self.file)
            self._width = max(self._width, len(s))
            self.file.flush()

    def finish(self):
        if self.file.isatty() and self.hide_cursor:
            print(SHOW_CURSOR, end='', file=self.file)


class WritelnMixin(object):
    hide_cursor = False

    def __init__(self, message=None, **kwargs):
        super(WritelnMixin, self).__init__(**kwargs)
        if message:
            self.message = message

        if self.file.isatty() and self.hide_cursor:
            print(HIDE_CURSOR, end='', file=self.file)

    def clearln(self):
        if self.file.isatty():
            print('\r\x1b[K', end='', file=self.file)

    def writeln(self, line):
        if self.file.isatty():
            self.clearln()
            print(line.encode('utf8'), end='', file=self.file)
            self.file.flush()

    def finish(self):
        if self.file.isatty():
            print(file=self.file)
            if self.hide_cursor:
                print(SHOW_CURSOR, end='', file=self.file)


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


def duration(seconds):
    days = int(seconds / 60 / 60 / 24)
    seconds = (seconds) % (60 * 60 * 24)
    hours = int((seconds / 60 / 60))
    seconds = (seconds) % (60 * 60)
    mins = int((seconds / 60))
    seconds = int((seconds) % (60))

    return (days, hours, mins, seconds)


def format_duration(duration):
    days, hours, mins, seconds = duration

    output = []

    if days:
        output.append("{0:d}d".format(days))
        output.append(" ")

    output.append("{0:d}:{1:d}:{2:d}".format(hours, mins, seconds))

    return "".join(output)
