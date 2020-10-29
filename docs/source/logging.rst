=============
Using Logging
=============

Logging are useful to know what really happened. All the logging are set to ``DEBUG``.
To view the ``DEBUG`` logs you would need to configure the ``logging`` module to show
``DEBUG`` logs as below.

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.DEBUG)
    import sxcu
    a=sxcu.SXCU()
 
Now all the debug logs are printed to ``stout``. You could also configure it to 
write to a file but that is out the scope of this documentation.
