Easy progress reporting for Python
==================================

Bars
----

There are 6 progress bars to choose from:

- Bar
- ChargingBar
- FillingSquaresBar
- FillingCirclesBar
- IncrementalBar
- ShadyBar

To use them, just call ``next`` to advance and ``finish`` to finish. ::

    from progress.bar import Bar

    bar = Bar('Processing', max=20)
    for i in range(20):
        # Do some work
        bar.next()
    bar.finish()

The result will be a bar like the following: ::

    Processing |#############                   | 42/100

To simplify the common case where the work is done in an iterator, you can
use the ``iter`` method. ::

    for i in Bar('Processing').iter(it):
        # Do some work

Progress bars are very customizable, you can change their width, their fill
character, their suffix and more. ::

    bar = Bar('Loading', fill='@', suffix='%(percent)d%%')

This will produce a bar like the following: ::

    Loading |@@@@@@@@@@@@@                   | 42%

You can use a number of template arguments in ``message`` and ``suffix``:

=========  =============================
Name       Value
=========  =============================
index      current value
max        maximum value
remaining  max - index
progress   index / max
percent    progress * 100
avg        rolling average time per item (in seconds)
eta        avg * remaining
=========  =============================

Instead of passing all configuration options on instatiation, you can create
your custom subclass. ::

    class FancyBar(Bar):
        message = 'Loading'
        fill = '*'
        suffix = '%(percent).1f%% - %(eta)ds'


Spinners
========

For actions with an unknown number of steps you can use a spinner. ::

    from progress.spinner import Spinner
    
    spinner = Spinner('Loading ')
    while state != 'FINISHED':
        # Do some work
        spinner.next()

There are 4 predefined spinners:

- Spinner
- PieSpinner
- MoonSpinner
- LineSpinner

Other
=====

Thera are a number of other classes available too, please check the source or
subclass one of them to create your own.
