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

To use them, just call ``next`` to advance and ``finish`` to finish:

.. code-block:: python

    from progress.bar import Bar

    bar = Bar('Processing', max=20)
    for i in range(20):
        # Do some work
        bar.next()
    bar.finish()

The result will be a bar like the following: ::

    Processing |#############                   | 42/100

To simplify the common case where the work is done in an iterator, you can
use the ``iter`` method:

.. code-block:: python

    for i in Bar('Processing').iter(it):
        # Do some work

Progress bars are very customizable, you can change their width, their fill
character, their suffix and more:

.. code-block:: python

    bar = Bar('Loading', fill='@', suffix='%(percent)d%%')

This will produce a bar like the following: ::

    Loading |@@@@@@@@@@@@@                   | 42%

You can use a number of template arguments in ``message`` and ``suffix``:

==========  ================================
Name        Value
==========  ================================
index       current value
max         maximum value
remaining   max - index
progress    index / max
percent     progress * 100
avg         simple moving average time per item (in seconds)
elapsed     elapsed time in seconds
elapsed_td  elapsed as a timedelta (useful for printing as a string)
eta         avg * remaining
eta_td      eta as a timedelta (useful for printing as a string)
==========  ================================

Instead of passing all configuration options on instatiation, you can create
your custom subclass:

.. code-block:: python

    class FancyBar(Bar):
        message = 'Loading'
        fill = '*'
        suffix = '%(percent).1f%% - %(eta)ds'

You can also override any of the arguments or create your own:

.. code-block:: python

    class SlowBar(Bar):
        suffix = '%(remaining_hours)d hours remaining'
        @property
        def remaining_hours(self):
            return self.eta // 3600


Spinners
========

For actions with an unknown number of steps you can use a spinner:

.. code-block::

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

There are a number of other classes available too, please check the source or
subclass one of them to create your own.
