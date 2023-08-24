import logging
import json
import os
import hashlib

from flask import current_app

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

    def use_default(self, imagePath):
        self.compile_favicon(imagePath)

    def compile_favicon(self, imagePath):
        if not os.path.exists(os.path.abspath(imagePath)):
            raise FileNotFoundError("{} could not be found".format(imagePath))

        outdir = make_compile_dir()

        favicon_checksum = sha256sum(imagePath)
        compiled_checksum = compiledsum(outdir)

        if favicon_checksum == compiled_checksum or not FORCE:
            return

        conf = {
            'app_name': self.app.name,
            'background_color': BACKGROUND_COLOR,
            'theme_color': THEME_COLOR
        }

        favicon = Image.open(imagePath)
        favicon_squared = transform_image_square(favicon)

        FaviconGroupStandard(conf, outdir).generate(favicon_squared)
        FaviconGroupAndroid(conf, outdir).generate(favicon_squared)
        FaviconGroupMS(conf, outdir).generate(favicon_squared)
        FaviconGroupApple(conf, outdir).generate(favicon_squared)
        FaviconGroupAppleStartup(conf, outdir).generate(favicon)
        FaviconGroupYandex(conf, outdir).generate(favicon_squared)

        self.compile_favicon_checksum(favicon_checksum, outdir)

    def compile_favicon_checksum(self, checksum, outdir):
        checksum_path = os.path.join(outdir, 'checksum')
        with open(checksum_path, 'w') as f:
            f.write(checksum)


def transform_image_square(image):
    width, height = image.size
    smaller_side = min(width, height)

    # Calculate padding values
    left = (width - smaller_side) // 2
    upper = (height - smaller_side) // 2
    right = width - (width - smaller_side - left)
    lower = height - (height - smaller_side - upper)

    padded_image = image.crop((left, upper, right, lower))
    return padded_image


def make_compile_dir():
    cdir = os.path.abspath('assets/favicon/')
    if not os.path.exists(cdir):
        os.mkdir(os.path.abspath('assets'))
        os.mkdir(os.path.abspath('assets/favicon'))
    return cdir


def compiledsum(outdir):
    try:
        with open(os.path.join(outdir, 'checksum.txt'), 'r') as f:
            compiled_checksum = f.read(64)
            return compiled_checksum
    except:
        return None


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
