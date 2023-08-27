from flask import g
import warnings


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
