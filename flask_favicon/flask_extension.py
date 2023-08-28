import os
import warnings
from pathlib import Path
from types import SimpleNamespace

from flask import Blueprint, g

from flask_favicon.flask_integration import favicon_url_for
from flask_favicon.flask_favicon_asset import FlaskFaviconAsset


class FlaskFavicon(object):
    def __init__(self, app=None):
        """
        Constructor function for FlaskFavicon. It will call
        :func:`FlaskFavicon.init_app` automatically if the
        app parameter is provided.

        :param app: A Flask application.
        :type app: flask.Flask
        """

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the extension.

        :param app: A Flask application.
        :type app: flask.Flask
        """

        self._registry = {}

        app.config.setdefault('FAVICON_BUILD_DIR', 'assets/favicon/')
        app.config.setdefault('FAVICON_DEFAULT_BACKGROUND_COLOR', '#ffffff')
        app.config.setdefault('FAVICON_DEFAULT_THEME_COLOR', '#000000')

        self.configuration = {
            'app_name': app.name,
            'background_color': app.config['FAVICON_DEFAULT_BACKGROUND_COLOR'],
            'theme_color': app.config['FAVICON_DEFAULT_THEME_COLOR'],
        }

        self.configuration['static_dir'] = _make_bp_static_dir(
            app.config['FAVICON_BUILD_DIR'])

        bp_favicon = Blueprint("flask-favicon", __name__,
                               template_folder='./templates',
                               static_url_path='/favicon',
                               static_folder=self.configuration['static_dir'])

        app.register_blueprint(bp_favicon)

        app.add_template_global(favicon_url_for, name="favicon_url_for")
        app.before_request(self._flask_favicon_before_request)

    def register_favicon(self, favicon_source_path=None, favicon_name='default',
                         background_color=None, theme_color=None):

        if not os.path.exists(os.path.abspath(favicon_source_path)):
            raise FileNotFoundError(
                "'{}' could not be found".format(favicon_source_path))

        favicon = FlaskFaviconAsset(
            favicon_source=favicon_source_path,
            favicon_name=favicon_name,
            background_color=background_color,
            theme_color=theme_color,
            configuration=self.configuration
        )

        self._registry[favicon_name] = favicon

        if not favicon.up_to_date:
            favicon.generate_assets()

    def _flask_favicon_before_request(self):
        g._flask_favicon = SimpleNamespace()
        g._flask_favicon.icon_registry = self._registry
        if 'default' not in g._flask_favicon.icon_registry.keys():
            warnings.warn(
                'Warning: The "{}" favicon was not registered during '
                'flask-favicon initialization.'.format('default'))
        else:
            g._flask_favicon.active_icon = self._registry['default']


def _make_bp_static_dir(build_dir):
    bp_static_dir = os.path.abspath(build_dir)
    Path(bp_static_dir).mkdir(parents=True, exist_ok=True)
    return bp_static_dir
