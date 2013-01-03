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

from __future__ import division
from __future__ import print_function

from signal import signal, SIGINT
from math import ceil
from sys import stderr, exit
from time import time


__version__ = '1.0.2'
__FILE__ = stderr


class Infinite(object):
    file = __FILE__
    avg_window = 10

    def __init__(self, *args, **kwargs):
        self.ctx = {}
        for key, val in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, val)
            else:
                self.ctx[key] = val

        self.index = 0
        self.avg = 0
        self._ts = time()

    def update_stats(self):
        # Calculate moving average
        now = time()
        dt = now - self._ts
        w = self.avg_window
        self.avg = dt if self.avg else (dt + w * self.avg) / (w + 1)
        self._ts = now

        kv = [(key, val) for key, val in self.__dict__.items()
                         if not key.startswith('_')]
        self.ctx.update(kv)

    def update(self):
        pass

    def start(self):
        pass

    def finish(self):
        pass

    def next(self):
        self.index = self.index + 1
        self.update_stats()
        self.update()

    def iter(self, it):
        for x in it:
            yield x
            self.next()
        self.finish()


class Progress(Infinite):
    backtrack = False

    def __init__(self, *args, **kwargs):
        super(Progress, self).__init__(*args, **kwargs)
        self.max = kwargs.get('max', 100)
        self.eta = 0

    def update_stats(self):
        self.progress = min(1, self.index / self.max)
        self.percent = self.progress * 100
        self.remaining = self.max - self.index

        # Calculate moving average
        now = time()
        if self.delta:
            dt = (now - self._ts) / self.delta
            w = self.avg_window
            self.avg = dt if self.avg else (dt + w * self.avg) / (w + 1)
            self.eta = int(ceil(self.avg * self.remaining))
        self._ts = now

        kv = [(key, val) for key, val in self.__dict__.items()
                         if not key.startswith('_')]
        self.ctx.update(kv)

    def start(self):
        self.delta = 0
        self.update_stats()
        self.update()

    def next(self):
        prev = self.index
        self.index = min(self.index + 1, self.max)
        self.delta = self.index - prev
        self.update_stats()
        self.update()

    def goto(self, index):
        index = min(index, self.max)
        delta = index - self.index
        if delta <= 0 and not self.backtrack:
            return

        self.index = index
        self.delta = delta
        self.update_stats()
        self.update()

    def iter(self, it):
        try:
            self.max = len(it)
        except TypeError:
            pass

        for x in it:
            yield x
            self.next()
        self.finish()


def _sig_term_handler(*args):
    show_cursor = '\x1b[?25h'
    print(show_cursor, end='', file=__FILE__)
    exit(0)

signal(SIGINT, _sig_term_handler)
