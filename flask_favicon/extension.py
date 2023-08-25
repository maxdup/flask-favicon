import functools
import logging
import json
import os
import hashlib
from pathlib import Path

from flask import Blueprint, url_for, g

from flask_favicon.favicon_ms import FaviconGroupMS
from flask_favicon.favicon_android import FaviconGroupAndroid
from flask_favicon.favicon_standard import FaviconGroupStandard
from flask_favicon.favicon_apple import FaviconGroupApple
from flask_favicon.favicon_apple_startup import FaviconGroupAppleStartup
from flask_favicon.favicon_yandex import FaviconGroupYandex

from PIL import Image
import json

EXT_NAME = "Flask-Favicon"
FORCE = True

BACKGROUND_COLOR = '#ffffff'
THEME_COLOR = '#000000'


class FlaskFavicon(object):
    def __init__(self, app=None):
        """
        Constructor function for FlaskFavicon. It will call
        :func:`FlaskFavicon.init_app` automatically if the
        app parameter is provided.

        :param app: A Flask application.
        :type app: flask.Flask
        """

        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the extension.

        :param app: A Flask application.
        :type app: flask.Flask
        """

        self.app = app

        self.static_dir = _make_bp_static_dir()
        bp_favicon = Blueprint("flask-favicon", __name__,
                               template_folder='./templates',
                               static_url_path='/favicon',
                               static_folder=self.static_dir)

        self.app.register_blueprint(bp_favicon)

        self.app.add_template_global(
            self.favicon_url_for, name="favicon_url_for")

        @app.before_request
        def flask_favicon_default():
            g.flask_favicon_active = 'default'

    def register_favicon(self, image_path, fav_name='default'):
        if not os.path.exists(os.path.abspath(image_path)):
            raise FileNotFoundError("{} could not be found".format(image_path))

        favicon_dir = _make_favicon_dir(self.static_dir, fav_name)

        favicon_checksum = _sha256sum(image_path)
        compiled_checksum = _compiledsum(favicon_dir)

        if favicon_checksum == compiled_checksum or not FORCE:
            return

        conf = {
            'app_name': self.app.name,
            'background_color': BACKGROUND_COLOR,
            'theme_color': THEME_COLOR
        }

        favicon = Image.open(image_path)

        favicon_groups = [FaviconGroupStandard, FaviconGroupAndroid,
                          FaviconGroupMS, FaviconGroupApple,
                          FaviconGroupAppleStartup, FaviconGroupYandex]

        for group in favicon_groups:
            group(conf, favicon_dir).generate(favicon)

        self.compile_favicon_checksum(favicon_checksum, favicon_dir)

    def favicon_url_for(self, filename=None):
        filename = filename or 'favicon.ico'
        filename = os.path.join(g.flask_favicon_active, filename)
        return url_for('flask-favicon.static', filename=filename)

    def compile_favicon_checksum(self, checksum, favicon_dir):
        checksum_path = os.path.join(favicon_dir, 'checksum')
        with open(checksum_path, 'w') as f:
            f.write(checksum)


def _make_bp_static_dir():
    bp_static_dir = os.path.abspath('assets/favicon/')
    Path(bp_static_dir).mkdir(parents=True, exist_ok=True)
    return bp_static_dir


def _make_favicon_dir(static_dir, fav_name):
    favicon_dir = os.path.join(static_dir, fav_name)
    Path(favicon_dir).mkdir(parents=True, exist_ok=True)
    return favicon_dir


def _compiledsum(favicon_dir):
    try:
        with open(os.path.join(favicon_dir, 'checksum.txt'), 'r') as f:
            compiled_checksum = f.read(64)
            return compiled_checksum
    except:
        return None


def _sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
