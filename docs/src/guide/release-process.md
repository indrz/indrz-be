# Release process

This document explains how to release Indrz. 
Inspiration taken/copied from the [Djangoproject Release How To](https://docs.djangoproject.com/en/dev/internals/howto-release-django/) as a great start.

**Please, keep these instructions up-to-date if you make changes!** The point
here is to be descriptive, not prescriptive, so feel free to streamline or
otherwise make changes, but **update this document accordingly!**

## Overview


There are three types of releases that you might need to make:

* Security releases: disclosing and fixing a vulnerability. This'll
  generally involve two or three simultaneous releases -- e.g.
  1.5.x, 1.6.x, and, depending on timing, perhaps a 1.7 alpha/beta/rc.

* Regular version releases: either a final release (e.g. 1.5) or a
  bugfix update (e.g. 1.5.1).

* Pre-releases: e.g. 1.6 alpha, beta, or rc.

The short version of the steps involved is:

1. If this is a security release, pre-notify the security distribution list
   one week before the actual release.

1. Proofread the release notes, looking for organization and writing errors.
   Draft a blog post and email announcement.

1. Update version numbers and create the release package(s).

1. Upload the new version(s) to PyPI.

1. Declare the new version in the admin on ``indrz.com``.

1. Post the blog entry and send out the email announcements.

1. Update version numbers post-release.

There are a lot of details, so please read on.


## Pre-release tasks

A few items need to be taken care of before even beginning the release process.
This stuff starts about a week before the release; most of it can be done
any time leading up to the actual release:

1. If this is a security release, send out pre-notification **one week** before
   the release. The template for that email and a list of the recipients are in
   the private ``indrz-security`` GitHub wiki. BCC the pre-notification
   recipients. Sign the email with the key you'll use for the release and
   include `CVE IDs <https://cveform.mitre.org/>`_ (requested with Vendor:
   indrzproject, Product: indrz) and patches for each issue being fixed.
   Also, :ref:`notify indrz-announce <security-disclosure>` of the upcoming
   security release.

1. Check with the other mergers to make sure they don't have any uncommitted
   changes for the release.

1. Proofread the release notes, including looking at the online version to
   :ref:`catch any broken links <documentation-link-check>` or reST errors, and
   make sure the release notes contain the correct date.

1. Double-check that the release notes mention deprecation timelines
   for any APIs noted as deprecated, and that they mention any changes
   in Python version support.

1. Double-check that the release notes index has a link to the notes
   for the new release; this will be in ``docs/releases/index.txt``.

1. If this is the alpha release of a new series, create a new stable branch
   from main. For example, when releasing indrz 3.1::

    $ git checkout -b stable/3.1.x origin/main
    $ git push origin -u stable/3.1.x:stable/3.1.x

   At the same time, update the ``indrz_next_version`` variable in
   ``docs/conf.py`` on the stable release branch to point to the new
   development version. For example, when creating ``stable/4.2.x``, set
   ``indrz_next_version`` to ``'5.0'`` on the new branch.

1. If this is the "dot zero" release of a new series, create a new branch from
   the current stable branch in the `indrz-docs-translations
   <https://github.com/indrz/indrz-docs-translations>`_ repository. For
   example, when releasing indrz 2.2::

    $ git checkout -b stable/2.2.x origin/stable/2.1.x
    $ git push origin stable/2.2.x:stable/2.2.x

## Preparing for release


Write the announcement blog post for the release. You can enter it into the
admin at any time and mark it as inactive. Here are a few examples: `example
security release announcement`__, `example regular release announcement`__,
`example pre-release announcement`__.

__ https://www.indrz.com/weblog/2013/feb/19/security/
__ https://www.indrz.com/weblog/2012/mar/23/14/
__ https://www.indrz.com/weblog/2012/nov/27/15-beta-1/

## Actually rolling the release


OK, this is the fun part, where we actually push out a release!

1. A release always begins from a release branch, so you should make sure
   you're on a stable branch and up-to-date. For example::

        $ git checkout stable/1.5.x
        $ git pull

1. If this is a security release, merge the appropriate patches from
   ``indrz-security``. Rebase these patches as necessary to make each one a
   plain commit on the release branch rather than a merge commit. To ensure
   this, merge them with the ``--ff-only`` flag; for example::

        $ git checkout stable/1.5.x
        $ git merge --ff-only security/1.5.x

   (This assumes ``security/1.5.x`` is a branch in the ``indrz-security`` repo
   containing the necessary security patches for the next release in the 1.5
   series.)

   If git refuses to merge with ``--ff-only``, switch to the security-patch
   branch and rebase it on the branch you are about to merge it into (``git
   checkout security/1.5.x; git rebase stable/1.5.x``) and then switch back and
   do the merge. Make sure the commit message for each security fix explains
   that the commit is a security fix and that an announcement will follow
   (:commit:`example security commit <bf39978a53f117ca02e9a0c78b76664a41a54745>`).

1. For a feature release, remove the ``UNDER DEVELOPMENT`` header at the
   top of the release notes and add the release date on the next line. For a
   patch release, replace ``*Under Development*`` with the release date. Make
   this change on all branches where the release notes for a particular version
   are located.

1. Update the version number in ``indrz/__init__.py`` for the release.
   Please see `notes on setting the VERSION tuple`_ below for details
   on ``VERSION``.

1. If this is a pre-release package, update the "Development Status" trove
   classifier in ``setup.cfg`` to reflect this. Otherwise, make sure the
   classifier is set to ``Development Status :: 5 - Production/Stable``.

1. Tag the release using ``git tag``. For example::

        $ git tag --sign --message="Tag 1.5.1" 1.5.1

   You can check your work by running ``git tag --verify <tag>``.

1. Push your work, including the tag: ``git push --tags``.

1. Make sure you have an absolutely clean tree by running ``git clean -dfx``.

1. Run ``make -f extras/Makefile`` to generate the release packages. This will
   create the release packages in a ``dist/`` directory.


If you're issuing multiple releases, repeat these steps for each release.

# Making the release(s) available to the public


Now you're ready to actually put the release out there. To do this:


1. Test that the release packages install correctly using ``pip``. Here's one
   method::

        $ RELEASE_VERSION='1.7.2'
        $ MAJOR_VERSION=`echo $RELEASE_VERSION| cut -c 1-3`

        $ python -m venv indrz-pip
        $ . indrz-pip/bin/activate
        $ python -m pip install https://www.indrz.com/m/releases/$MAJOR_VERSION/indrz-$RELEASE_VERSION.tar.gz
        $ deactivate
        $ python -m venv indrz-pip-wheel
        $ . indrz-pip-wheel/bin/activate
        $ python -m pip install https://www.indrz.com/m/releases/$MAJOR_VERSION/indrz-$RELEASE_VERSION-py3-none-any.whl
        $ deactivate

   This just tests that the tarballs are available (i.e. redirects are up) and
   that they install correctly, but it'll catch silly mistakes.

1. Upload the release packages to PyPI (for pre-releases, only upload the wheel
   file)::

       $ twine upload -s dist/*

1. Make the blog post announcing the release live.

1. For a new version release (e.g. 1.5, 1.6), update the default stable version
   of the docs by flipping the ``is_default`` flag to ``True`` on the
   appropriate ``DocumentRelease`` object in the ``docs.indrz.com``
   database (this will automatically flip it to ``False`` for all
   others); you can do this using the site's admin.

   Create new ``DocumentRelease`` objects for each language that has an entry
   for the previous release. Update indrz.com's `robots.docs.txt`__
   file by copying entries from ``manage_translations.py robots_txt`` from the
   current stable branch in the ``indrz-docs-translations`` repository. For
   example, when releasing indrz 2.2::

        $ git checkout stable/2.2.x
        $ git pull
        $ python manage_translations.py robots_txt

   __ https://github.com/indrz/indrz.com/blob/main/indrzproject/static/robots.docs.txt

1. Post the release announcement to the |indrz-announce|, |indrz-developers|,
   and |indrz-users| mailing lists. This should include a link to the
   announcement blog post.

1. If this is a security release, send a separate email to
   oss-security@lists.openwall.com. Provide a descriptive subject, for example,
   "indrz" plus the issue title from the release notes (including CVE ID). The
   message body should include the vulnerability details, for example, the
   announcement blog post text. Include a link to the announcement blog post.

1. Add a link to the blog post in the topic of the ``#indrz`` IRC channel:
   ``/msg chanserv TOPIC #indrz new topic goes here``.

## Post-release

You're almost done! All that's left to do now is:

1. Update the ``VERSION`` tuple in ``indrz/__init__.py`` again,
   incrementing to whatever the next expected release will be. For
   example, after releasing 1.5.1, update ``VERSION`` to
   ``VERSION = (1, 5, 2, 'alpha', 0)``.

1. If this was a security release, update :doc:`/releases/security` with
   details of the issues addressed.


## New stable branch tasks

There are several items to do in the time following the creation of a new
stable branch (often following an alpha release). Some of these tasks don't
need to be done by the releaser.

1. Create a new ``DocumentRelease`` object in the ``docs.indrz.com``
   database for the new version's docs, and update the
   ``docs/fixtures/doc_releases.json`` JSON fixture, so people without access
   to the production DB can still run an up-to-date copy of the docs site.

1. Create a stub release note for the new feature version. Use the stub from
   the previous feature release version or copy the contents from the previous
   feature version and delete most of the contents leaving only the headings.

1. Remove features that have reached the end of their deprecation cycle. Each
   removal should be done in a separate commit for clarity. In the commit
   message, add a "refs #XXXX" to the original ticket where the deprecation
   began if possible.

1. Remove ``.. versionadded::``, ``.. versionadded::``, and ``.. deprecated::``
   annotations in the documentation from two releases ago. For example, in
   indrz 1.9, notes for 1.7 will be removed.

1. Add the new branch to `Read the Docs
   <https://readthedocs.org/projects/indrz/>`_. Since the automatically
   generated version names ("stable-A.B.x") differ from the version names
   used in Read the Docs ("A.B.x"), `create a ticket
   <https://github.com/readthedocs/readthedocs.org/issues/5537>`_ requesting
   the new version.

1. `Request the new classifier on PyPI
   <https://github.com/pypa/trove-classifiers/issues/29>`_. For example
   ``Framework :: indrz :: 3.1``.

##  Notes on setting the VERSION tuple

indrz's version reporting is controlled by the ``VERSION`` tuple in
``indrz/__init__.py``. This is a five-element tuple, whose elements
are:

1. Major version.
1. Minor version.
1. Micro version.
1. Status -- can be one of "alpha", "beta", "rc" or "final".
1. Series number, for alpha/beta/RC packages which run in sequence
   (allowing, for example, "beta 1", "beta 2", etc.).

For a final release, the status is always "final" and the series
number is always 0. A series number of 0 with an "alpha" status will
be reported as "pre-alpha".

Some examples:

* ``(1, 2, 1, 'final', 0)`` → "1.2.1"

* ``(1, 3, 0, 'alpha', 0)`` → "1.3 pre-alpha"

* ``(1, 3, 0, 'beta', 2)`` → "1.3 beta 2"