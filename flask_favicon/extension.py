import logging
import json
import os

from flask import request, url_for

EXT_NAME = "Flask-Favicon"


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
