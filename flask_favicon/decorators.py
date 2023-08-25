from flask import g


def use_favicon(favicon_name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            g.flask_favicon_active = favicon_name
            return fn(*args, **kwargs)
        return wrapper
    return decorator
