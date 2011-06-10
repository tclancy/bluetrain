This is a very simple Django CMS application. It allows for the creation of hierarchical pages, adding "focus areas" to the pages along with normal content.
There is also a view for displaying a sitemap (all of the pages tied to home). It relies heavily on terminology from my old web dev days, so it
includes three types of pages:
1. Home page -- there should only be one and it should have a slug of 'home'
2. Normal pages -- you get it
3. Constants -- these are pages that do not appear in the page hierarchy but can be visited by all,
typically links that appear on all pages, e.g., 'contact us'

INSTALL
=======

You will want to load both files under fixtures via ./manage.py loaddata

REQUIRED SETTINGS
=================

USE_CACHE: whether to use Django's caching or not
DEFAULT_CACHE_TIMEOUT: number of seconds to cache items

Neither of these settings should be required and I should be providing backup/ defaults for you. Kick me if you are reading this.

TEMPLATE TAGS
=============

There's a single tag in there right now for rendering forms based on the display in default_form.html.
Override this template as needed.

TODO
====
* More tests, obviously
* Default settings