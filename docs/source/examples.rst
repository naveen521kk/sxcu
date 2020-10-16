========
Examples
========

Uploading a Image to sxcu.net
*****************************

To upload an image `foo.png` located in the same directory as the script and print the url:

.. code-block:: python

    import sxcu
    connector = sxcu.SXCU()
    result = connector.upload_image("foo.png")
    print(result["url"])

Parameters acceped are

.. currentmodule:: sxcu

.. autosummary::
   :recursive:

    ~SXCU.upload_image

Uploading Image with ``og_properties``
**************************************

What is ``og_properties``?
--------------------------

`The Open Graph protocol <https://ogp.me/>`_ The Open Graph protocol enables any web page to become a rich object in a social graph.

`sxcu.net <https://sxcu.net>`_ allows the following properties to be changed for changing the way it embed in apps and websites.

How to use it?
--------------

Using the class

.. autosummary::

    ~og_properties

A small example using this can be

.. code-block:: python

    import sxcu
    connector = sxcu.SXCU()
    props = sxcu.og_properties(color="#000",description="some random post",title="I love SXCU")
    result = connector.upload_image("foo.png")
    print(result["url"])

Creating a Short Link
*********************

The reference for it is

.. autosummary::

    ~SXCU.create_link

A small example illustrating it can be.

.. code-block:: python

    import sxcu
    connector = sxcu.SXCU()
    result = connector.create_link("https://sxcu.syrusdark.website")
    print(result["url"])

should print a shortened URL.
