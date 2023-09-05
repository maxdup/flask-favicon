[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/flask-favicon.svg)](https://pypi.python.org/pypi/flask-favicon/)
[![Platforms](https://img.shields.io/badge/platform-Linux,_MacOS,_Windows-blue)]()
[![PyPI version fury.io](https://badge.fury.io/py/flask-favicon.svg)](https://pypi.python.org/pypi/flask-favicon/)
[![GitHub Workflow Status (with event)](https://github.com/maxdup/flask-favicon/actions/workflows/CI.yml/badge.svg)]()
[![Coverage](https://github.com/maxdup/flask-favicon/blob/main/docs/source/coverage.svg "coverage")]()

# Flask-favicon


Flask-favicon is a [Flask](https://flask.palletsprojects.com) extension which generates multiple favicon variants for different platforms. The goal is to cover as many devices as possible from a single image file. Flask-favicon serves all the assets for you and provides an easy to use Jinga template which you can include in your html `<head>`.

Full Documentation: https://maxdup.github.io/flask-favicon/


## Installation

Flask-favicon is available on the Python Package Index. This makes installing it with pip as easy as:

```bash
pip install flask-favicon
```



Initializing
------------

The extension needs to be loaded alongside your Flask application. All favicons need to be declared during app creation with `register_favicon()`. You may register any amount of favicons. You should have at least one favicon named as `'default'`

Here's a minimal example of how this is done:

```python
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
```


Usage
-----

Initiallizing `FlaskFavicon` provides you with a Jinga template to be inserted in your `<head>`.

```html
<!-- _head.html -->
<head>
    ...
    {% include "flask-favicon.html" %}
    ...
</head>
```

By default, the `flask-favicon.html` template will be populated with the favicon registered as `'default'`.

To use the alternative favicons as declared earlier, you can use Flask-favicon's `use_favicon` decorator alongside route declarations.

```python

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
```

> **_NOTE:_** `@use_favicon()` comes after the `@bp.route()` decorator.