import pytest
from flask import Flask, Blueprint, testing, jsonify, make_response
from flask_favicon import FlaskFavicon


class TestClient(testing.FlaskClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def create_app():
    flaskapp = Flask('flask-ext')

    flaskapp.config.update({
        'TEST': True,
    })
    flaskapp.url_map.strict_slashes = True
    flaskapp.test_client_class = TestClient

    @flaskapp.route('/')
    def mockRoute():
        return make_response(jsonify.dumps({}), 200)

    return flaskapp


@pytest.fixture
def appFactory():
    return create_app


@pytest.fixture
def app(appFactory):
    flaskapp = appFactory()

    flaskFavicon = FlaskFavicon()
    flaskFavicon.init_app(flaskapp)

    yield flaskapp


@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            yield client
