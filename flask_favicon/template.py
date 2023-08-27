import os
from flask import g, url_for


def favicon_url_for(filename=None):
    filename = filename or 'favicon.ico'
    filename = os.path.join(g._flask_favicon.activeIcon.favicon_name, filename)
    return url_for('flask-favicon.static', filename=filename)
