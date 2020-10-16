:tocdepth: 1

.. _changes:

*********
Changelog
*********

sxcu-v2.0.1
===========

[TOB]

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
