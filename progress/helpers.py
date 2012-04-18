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


class WriteMixin(object):
    def __init__(self, message=None, **kwargs):
        super(WriteMixin, self).__init__(**kwargs)
        self._width = 0
        if message:
            self.message = message

        if self.file.isatty():
            print(self.message, end='', file=self.file)
            self.file.flush()

    def write(self, s):
        if self.file.isatty():
            b = '\b' * self._width
            print(b + s.ljust(self._width), end='', file=self.file)
            self._width = max(self._width, len(s))
            self.file.flush()


class WritelnMixin(object):
    def __init__(self, message=None, **kwargs):
        super(WritelnMixin, self).__init__(**kwargs)
        self.max_line_width = 0
        if message:
            self.message = message

    def writeln(self, line):
        if not self.file.isatty():
            return
        if len(line) > self.max_line_width:
            self.max_line_width = len(line)
        else:
            line += ' ' * (self.max_line_width - len(line))     # Add padding

        print('\r' + line, end='', file=self.file)
        self.file.flush()

    def finish(self):
        if self.file.isatty():
            print(file=self.file)
