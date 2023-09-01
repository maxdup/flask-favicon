Quickstart
==========

Get yourself up and running quickly.

Installation
------------

PyPI
~~~~
flask-favicon is available on the Python Package Index. This makes installing it with pip as easy as:

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

The extension needs to be loaded alongside your Flask application.

Here's how it's done:

.. code-block:: python

    from flask import Flask, Blueprint
    from flask_favicon import FlaskFavicon

    flaskFavicon = FlaskFavicon()

    app = Flask('my-app',
                static_folder='dist/static',
                static_url_path='/static')

    bp = Blueprint('my-blueprint',
                   __name__,
                   static_folder='blueprints/static',
                   static_url_path='/bp/static')

    app.register_blueprint(bp)

    flaskFavicon.init_app(app)
    flaskFavicon.register_favicon('source/favicon.png', 'default')

    app.run()

Usage
-----

Flask-favicon adds the :any:`use_favicon` route decorator for use in app.

.. code-block:: python

   @use_favicon
   def index():
       pass
