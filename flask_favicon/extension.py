import functools
import logging
import json
import os
import hashlib
import warnings
from pathlib import Path
from types import SimpleNamespace

from flask import Blueprint, url_for, g

from flask_favicon.favicon_ms import FaviconGroupMS
from flask_favicon.favicon_android import FaviconGroupAndroid
from flask_favicon.favicon_standard import FaviconGroupStandard
from flask_favicon.favicon_apple import FaviconGroupApple
from flask_favicon.favicon_apple_startup import FaviconGroupAppleStartup
from flask_favicon.favicon_yandex import FaviconGroupYandex

from flask_favicon.template import favicon_url_for

from PIL import Image
import json


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

            'build_dir': app.config['FAVICON_BUILD_DIR'],
        }

        self.configuration['static_dir'] = _make_bp_static_dir(
            self.configuration['build_dir'])

        bp_favicon = Blueprint("flask-favicon", __name__,
                               template_folder='./templates',
                               static_url_path='/favicon',
                               static_folder=self.configuration['static_dir'])

        app.register_blueprint(bp_favicon)
        app.add_template_global(favicon_url_for, name="favicon_url_for")

        @app.before_request
        def flask_favicon_default():
            g._flask_favicon = SimpleNamespace()
            g._flask_favicon.iconRegistry = self._registry
            if 'default' not in g._flask_favicon.iconRegistry.keys():
                warnings.warn(
                    'Warning: The "{}" favicon was not registered during '
                    'flask-favicon initialization.'.format('default'))
            else:
                g._flask_favicon.activeIcon = self._registry['default']

    def register_favicon(self, favicon_source_path=None, favicon_name='default',
                         background_color=None, theme_color=None):

        if not os.path.exists(os.path.abspath(favicon_source_path)):
            raise FileNotFoundError(
                "{} could not be found".format(favicon_source_path))

        favicon = FlaskFaviconAsset(
            favicon_name=favicon_name,
            favicon_source=favicon_source_path,
            background_color=background_color,
            theme_color=theme_color,
            configuration=self.configuration
        )

        if not favicon.up_to_date:
            favicon.generate_assets()

        self._registry[favicon_name] = favicon


class FlaskFaviconAsset(object):
    def __init__(self, favicon_name, favicon_source, configuration,
                 background_color=None, theme_color=None):

        self.favicon_name = favicon_name
        self.favicon_source = favicon_source
        self.favicon_dir = self._make_favicon_dir(
            favicon_name, configuration['static_dir'])
        self.configuration = configuration

        self.background_color = background_color
        if not self.background_color:
            self.background_color = configuration['background_color']

        self.theme_color = theme_color
        if not self.theme_color:
            self.theme_color = configuration['theme_color']

        # Check if compile required
        self._source_checksum = self._sha256sum(self.favicon_source)
        self._built_checksum = self._compiledsum(self.favicon_dir)

        self.up_to_date = self._source_checksum == self._built_checksum

    def generate_assets(self):
        favicon = Image.open(self.favicon_source)

        favicon_groups = [FaviconGroupStandard, FaviconGroupAndroid,
                          FaviconGroupMS, FaviconGroupApple,
                          FaviconGroupAppleStartup, FaviconGroupYandex]

        for group in favicon_groups:
            group(self.configuration, self.favicon_dir).generate(favicon)

        self.compile_favicon_checksum(self._source_checksum, self.favicon_dir)

    def compile_favicon_checksum(self, checksum, favicon_dir):
        checksum_path = os.path.join(self.favicon_dir, 'checksum')
        with open(checksum_path, 'w') as f:
            f.write(checksum)

    def _make_favicon_dir(self, favicon_name, static_dir):
        favicon_dir = os.path.join(static_dir, favicon_name)
        Path(favicon_dir).mkdir(parents=True, exist_ok=True)
        return favicon_dir

    def _compiledsum(self, favicon_dir):
        try:
            with open(os.path.join(favicon_dir, 'checksum.txt'), 'r') as f:
                compiled_checksum = f.read(64)
                return compiled_checksum
        except:
            return None

    def _sha256sum(self, filename):
        h = hashlib.sha256()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()


def _make_bp_static_dir(build_dir):
    bp_static_dir = os.path.abspath(build_dir)
    Path(bp_static_dir).mkdir(parents=True, exist_ok=True)
    return bp_static_dir
