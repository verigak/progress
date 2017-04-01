#!/usr/bin/env python

from __future__ import print_function

import random
import time

from progress.bar import (Bar, ChargingBar, FillingSquaresBar, AdaptiveBar,
                          FillingCirclesBar, IncrementalBar, ShadyBar)
from progress.spinner import Spinner, PieSpinner, MoonSpinner, LineSpinner
from progress.counter import Counter, Countdown, Stack, Pie


def sleep():
    t = 0.01
    t += t * random.uniform(-0.1, 0.1)  # Add some variance
    time.sleep(t)

for bar_cls in (Bar, ChargingBar, FillingSquaresBar, FillingCirclesBar):
    suffix = '%(index)d/%(max)d [%(elapsed)d / %(eta)d / %(eta_td)s]'
    bar = bar_cls(bar_cls.__name__, suffix=suffix)
    for i in bar.iter(range(200)):
        sleep()

for bar_cls in (IncrementalBar, ShadyBar):
    suffix = '%(percent)d%% [%(elapsed_td)s / %(eta)d / %(eta_td)s]'
    bar = bar_cls(bar_cls.__name__, suffix=suffix)
    for i in bar.iter(range(200)):
        sleep()

for bar_cls in [AdaptiveBar]:
    suffix = '%(index)d%% [%(elapsed_td)s]'
    bar = bar_cls(bar_cls.__name__, suffix=suffix)
    for i in bar.iter(range(200)):
        sleep()
    print()

for spin in (Spinner, PieSpinner, MoonSpinner, LineSpinner):
    for i in spin(spin.__name__ + ' ').iter(range(100)):
        sleep()
    print()

for singleton in (Counter, Countdown, Stack, Pie):
    for i in singleton(singleton.__name__ + ' ').iter(range(100)):
        sleep()
    print()

bar = IncrementalBar('Random', suffix='%(index)d')
for i in range(100):
    bar.goto(random.randint(0, 100))
    sleep()
bar.finish()
