=======================================
Sphinx extension "sphinx-contrib.slide"
=======================================

:Author:          Martin Bless <martin.bless@mbless.de>
:Original author: Takeshi Komiya (`tk0miya <https://github.com/tk0miya>`_)
:Original repo:   https://github.com/sphinx-contrib/slide/, kept in branch
                  `tk0miya
                  <https://github.com/TYPO3-Documentation/sphinx-contrib-slide/tree/tk0miya>`__

:Version:         1.0
:Release:         1.0.0


What is it?
===========

This is a sphinx extension for embedding your presentation slides, Google
documents and Google spreadsheets.

What can be embedded?
---------------------

#. `Google docs <https://docs.google.com/>`_ documents
#. `Google docs`_ presentations
#. `Google docs`_ spreadsheets
#. `Slides.com <https://slides.com/>`_ presentations
#. `Slideshare <https://www.slideshare.net/>`_ presentations
#. `Speakerdeck <https://speakerdeck.com/>`_ presentations

Syntax
------

`.. slide:: URL`

URL must be one of these::

   https://docs.google.com/document/d/…
   https://docs.google.com/presentation/d/…
   https://docs.google.com/spreadsheets/d/…
   https://slides.com/…          or http://…
   https://speakerdeck.com/…
   https://www.slideshare.net/…  or http://…

Tip
---

*Finding the URL:* For Google docs go to ① "File", ② "Publish to the web",
③ and "Link" or ④ copy the basic part of the link from your browser.


Code and contributing
=====================

Please find `the repository
<https://github.com/TYPO3-Documentation/sphinx-contrib-slide>`__ at Github.

For contributions please add an `issue
<https://github.com/TYPO3-Documentation/sphinx-contrib-slide/issues>`_ there or
provide a pull request.


Examples
========

.. code-block:: rst

   .. slide:: https://docs.google.com/document/d/e/2PACX-1vR-lBF77A6YgK77uE8wzxFNbtxnS98I3DXSMW5qajO02QfkIc5vAdi10_iJMvXAmPJvv2Sedo_HllHE/pub

   .. slide:: https://docs.google.com/presentation/d/1FOVjpJIJrHC4Wly9rsGelDdfXe4bgamLOJh1GlVx2Tk

   .. slide:: https://docs.google.com/spreadsheets/d/e/2PACX-1vRBBypnQdGwdTCq6Xz2EJyySm1v_Q0XndMlmFwHgjBAbxHuVQGNgch3qr9neSX66GjSAA_x8tZldqD5/pubhtml

   .. slide:: https://slides.com/bolajiayodeji/introduction-to-version-control-with-git-and-github

   .. slide:: https://www.slideshare.net/TedTalks/physics-45280434

   .. slide:: https://speakerdeck.com/oliverklee/test-driven-development-with-phpunit-1


Setting up the extension
========================

Installation
------------

Install the Python package from the repository:

.. code-block:: shell

   # set a proper release
   RELEASE_ARCHIVE=0.3.0.zip
   RELEASE_ARCHIVE=0.3.1.zip
   RELEASE_ARCHIVE=1.0.0.zip
   pipenv install https://github.com/sphinx-contrib/slide/archive/$RELEASE_ARCHIVE

Verify: Make sure the 'slide' module can be loaded. The following command
should run without error:

.. code-block:: shell

   python -c "import sphinxcontrib.slide"


Configure Sphinx
----------------

To enable this extension, add ``sphinxcontrib.slide`` module to the extensions
option at :file:`conf.py`.

.. code-block:: python

   # Enabled extensions
   extensions = ['sphinxcontrib.slide']


Using the directive
-------------------

Currently the directive only takes a single parameter 'URL':

.. code-block: rst

   .. slide:: URL


Optional CSS
------------

Consider adding the following CSS to your theme. It will stretch the width
to 100 percent and react responsively keeping the aspect ratio.

.. code-block::

   .iframe-box {
       height: 0;
       max-width: 100%;
       overflow: hidden;
       padding-bottom: 56.25%;  /* 16:9 */
       padding-top: 35px;
       position: relative;
       position: relative;
       width: 100%;
   }

   .iframe-box iframe {
       height: 100%;
       left: 0;
       position: absolute;
       top:0;
       width: 100%;
   }
   .iframe-box-slideshare {
       padding-bottom: 75.5%;  /* derived experimentally */
   }


End of README.