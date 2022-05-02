:tocdepth: 1

.. _changes:

*********
Changelog
*********

sxcu-v4.1.0
===========

New Features
------------

* Allow uploading a file directly from :class:`io.BytesIO`, see ``fileobj`` parameter in :func:`sxcu.SXCU.upload_file`
* Allow passing :class:`io.StringIO` file as config file in :class:`.SXCU`


Other changes
-------------

* Deprecate ``file_sxcu`` in :class:`.SXCU`, use ``sxcu_config`` instead.
* Deprecate ``file`` parameter in :func:`sxcu.SXCU.upload_file`, use ``name`` instead.


sxcu-v4.0.0
===========

This contains support for sxcu.net API v2.

Breaking changes
----------------

* Removed support for sxcu.net API v1 which is deprecated and would
  be removed soon.
* Remove ``edit_collection`` method. I was informed it was to be removed
  soon from the API.
* A default logging handler which print debug info is removed. 
  Please set up your own handler. Details at :ref:`Using Logging`.
* Deprecate :attr:`~.SXCU.upload_image`. Use :attr:`~.SXCU.upload_file`
  instead.
* Deprecate :attr:`~.SXCU.collection_details`. Use :attr:`~.SXCU.collection_meta`
  instead.
* Deprecate :attr:`~.SXCU.image_details`. Use :attr:`~.SXCU.file_meta`
  instead.
* Deprecate :attr:`~.SXCU.domain_list`. Use :attr:`~.SXCU.list_subdomain`
  instead.

New Features
------------

* Added support for :attr:`~.OGProperties.site_name` in :class:`~.OGProperties`
* Added support for ``self_destruct`` in :attr:`~.SXCU.upload_file`.

Bug fixes
---------

* Fix ``sxcu.__version__`` printing displaying wrong version.


Other changes
-------------

* Miscellaneous typo fixes.
* Slightly improve language in request handler.
* Changed the default user agent to contain a URL to this project.

sxcu-v3.2.0
===========

* Update for new API changes

sxcu-v3.1.0
===========

* Added ``OGProperties.from_json()`` method.
* Fix broken Error Handler. It raises :class:`SXCUError` when 
  there is an error from server now.
* Update API details. (slightly)

sxcu-v3.0.0
===========

* Rename ``og_properties`` to ``OGProperties``.
* Add support for ``discord_hide_url``.

sxcu-v2.0.0
===========

* Introduced a logger class so that users can know what
  really happened. User's can just set a logging handle and
  it will automatically write logs as in any other library.

* Improved Interface with Requests. Instead of Directly
  calling it now logs them and goes through ``__client__``.

* Moved version to ``__version__`` and added other meta data
  to it.

* Now it handle's server response codes. Previously it was
  rising JSON decode Error which was unexpected and could cause
  problems.


sxcu-v1.0.1
===========

* Fixed an issue in reading ``.sxcu`` file. (PR-10)
* Fixed ``__version__`` and removed a dependency.

sxcu-v1.0.0
===========

New Features
------------

* Create a new logo.
* Added a missing API method :func:`~.SXCU.image_details`.
* Fix a bug due to subdomain parsing while using ``.sxcu`` files.
* Add a missing endpoint of :func:`edit_collection`.
* Fixed a bug in :func:`create_link`


For developers
--------------

* Added docs at https://sxcu.syrusdark.website.
* Added a few Tests.
* Enforce formatting with pre-commit.
* Added test Coverage
* Linting For Pull Requests Added.

sxcu-v0.1.0-alpha.0
===================

Initial release with basic structure.
