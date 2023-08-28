import os
import warnings

from flask import g, url_for


def use_favicon(favicon_name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if favicon_name not in g._flask_favicon.iconRegistry.keys():
                warnings.warn(
                    'Warning: The "{}" favicon was not registered during '
                    'flask-favicon initialization.'.format(favicon_name))
            else:
                g._flask_favicon.activeIcon = g._flask_favicon.iconRegistry[favicon_name]

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def favicon_url_for(filename=None):
    filename = filename or 'favicon.ico'
    filename = os.path.join(g._flask_favicon.activeIcon.favicon_name, filename)
    return url_for('flask-favicon.static', filename=filename)
