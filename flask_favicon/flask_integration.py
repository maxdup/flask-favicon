import os
import warnings

from flask import g, url_for


def use_favicon(favicon_name):
    '''
    Function decorator to override the default favicon on a specific route.

    :param favicon_name: The identifier of the favicon to be used.
    :type favicon_name: str
    '''
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if favicon_name not in g._flask_favicon.icon_registry.keys():
                warnings.warn(
                    'Warning: The "{}" favicon was not registered during '
                    'flask-favicon initialization.'.format(favicon_name))
            else:
                g._flask_favicon.active_icon = g._flask_favicon.icon_registry[favicon_name]

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def favicon_url_for(filename=None):
    filename = filename or 'favicon.ico'
    filename = os.path.normpath(os.path.join(
        g._flask_favicon.active_icon.favicon_name, filename))
    return url_for('flask-favicon.static', filename=filename)
