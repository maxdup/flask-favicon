Quickstart
==========

Get yourself up and running quickly.

Installation
------------

PyPI
~~~~

Flask-favicon is available on the Python Package Index. This makes installing it with pip as easy as:

.. code-block:: bash

   pip install flask-favicon

Git
~~~

If you want the latest code or even feel like contributing, the code is available on GitHub.

You can easily clone the code with git:

.. code-block:: bash

   git clone git://github.com/maxdup/flask-favicon.git

and install it from the repo directory with:

.. code-block:: bash

   python setup.py install
   # or
   pip install .


Initializing
------------

The extension needs to be loaded alongside your Flask application. All favicons need to be declared during app creation with :any:`register_favicon<FlaskFavicon.register_favicon()>`. You may register any amount of favicons. You should have at least one favicon named as :code:`'default'`

Here's a minimal example of how this is done:

.. code-block:: python

    from flask import Flask, Blueprint
    from flask_favicon import FlaskFavicon

    flaskFavicon = FlaskFavicon()

    app = Flask('my-app')

    bp = Blueprint('my-blueprint', __name__)
    app.register_blueprint(bp)

    flaskFavicon.init_app(app)
    flaskFavicon.register_favicon('source/favicon.png', 'default') # filename, favicon identifier
    flaskFavicon.register_favicon('source/favicon-alt.png', 'default-alt')
    flaskFavicon.register_favicon('source/promo.png', 'promo')

    app.run()

Usage
-----

Initiallizing :code:`FlaskFavicon` provides you with a Jinga template to be inserted in your :code:`<head>`.

.. code-block:: jinga

    <!-- _head.html -->
    <head>
      ...
      {% include "flask-favicon.html" %}
      ...
    </head>

By default, the :code:`flask-favicon.html` template will be populated with the favicon registered as :code:`'default'`.

To use the alternative favicons as declared earlier, you can use Flask-favicon's :any:`use_favicon` decorator alongside route declarations.

.. code-block:: python

   from flask import Blueprint, render_template
   from flask_favicon import use_favicon

   bp_site = Blueprint('site', __name__)

   @bp_site.route("/")
   # will use 'default' favicon
   def index():
       return render_template('index.html')

   @bp_site.route("/promo")
   @use_favicon('promo')
   def promo():
       return render_template('promo-page.html')

   @bp_site.route("/special-event")
   @use_favicon('default-alt')
   def special_event():
       return render_template('special-page.html')

.. note::

   :code:`@use_favicon()` comes after the :code:`@bp.route()` decorator.
