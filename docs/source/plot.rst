Plotting.
---------

Plot the findings.
~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :linenos:
       
    ```
    >>> from pyharmonics.plotter import Plotter
    >>> p = Plotter(t, 'BTCUSDT', b.HOUR_1)
    >>> p.add_matrix_plots(m.get_patterns(family=m.XABCD))
    >>> p.show()
    ```

You will see something like this.

.. image:: images/newplot.png
  :alt: Fully formed patterns

See all harmonic patterns.
~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :linenos:
       
    ```
    >>> p = Plotter(t, 'BTCUSDT', b.HOUR_1)
    >>> p.add_matrix_plots(m.get_patterns())
    >>> p.show()
    ```

You will see something like this.

.. image:: images/all_patterns.png
  :alt: Fully formed patterns

See all forming patterns.
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python
    :linenos:
       
    ```
    >>> m = MatrixSearch(t)
    >>> m.forming()
    >>> p = Plotter(t, 'BTCUSDT', b.HOUR_1)
    >>> p.add_matrix_plots(m.get_patterns(formed=False))
    >>> p.show()
    ```
etc.