from unittest import mock

from flask import g

from flask_favicon.flask_integration import use_favicon, favicon_url_for
from flask_favicon.flask_extension import FlaskFavicon


@mock.patch('pathlib.Path.mkdir')
@mock.patch('flask_favicon.flask_favicon_asset.FlaskFaviconAsset.generate_assets')
def test_use_favicon_decorator(mock_generate, mock_mkdir, appFactory):

    app = appFactory()

    flaskFavicon = FlaskFavicon()
    flaskFavicon.init_app(app)

    def decorated(*args, **kwargs):
        pass

    # without default
    with app.test_request_context('/') as ctx:
        app.preprocess_request()

        with mock.patch('warnings.warn') as mock_warn:

            decorator = use_favicon('default')
            decorator(decorated)(decorated)

            mock_warn.assert_called_once_with(
                'Warning: The "default" favicon was not registered during '
                'flask-favicon initialization.'
            )
            mock_warn.reset_mock()

    # with missing
    flaskFavicon.register_favicon('tests/data/favicon1.png', 'default')
    with app.test_request_context('/') as ctx:
        app.preprocess_request()

        with mock.patch('warnings.warn') as mock_warn:

            decorator = use_favicon('missing')
            decorator(decorated)(decorated)
            mock_warn.assert_called_once()
            mock_warn.assert_called_once_with(
                'Warning: The "missing" favicon was not registered during '
                'flask-favicon initialization.'
            )
            assert g._flask_favicon.active_icon == g._flask_favicon.icon_registry['default']
            mock_warn.reset_mock()

    # with default
    flaskFavicon.register_favicon('tests/data/favicon2.png', 'default-alt')

    with app.test_request_context('/') as ctx:
        app.preprocess_request()
        with mock.patch('warnings.warn') as mock_warn:

            decorator = use_favicon('default')
            mock_warn.assert_not_called()
            assert g._flask_favicon.active_icon == g._flask_favicon.icon_registry['default']

            decorator = use_favicon('default-alt')
            decorator(decorated)(decorated)
            mock_warn.assert_not_called()
            assert g._flask_favicon.active_icon == g._flask_favicon.icon_registry['default-alt']


@mock.patch('pathlib.Path.mkdir')
@mock.patch('flask_favicon.flask_favicon_asset.FlaskFaviconAsset.generate_assets')
def test_favicon_url_for(mock_generate, mock_mkdir, appFactory):

    app = appFactory()

    flaskFavicon = FlaskFavicon()
    flaskFavicon.init_app(app)
    flaskFavicon.register_favicon('tests/data/favicon1.png', 'default')
    flaskFavicon.register_favicon('tests/data/favicon1.png', 'default-alt')
    flaskFavicon.register_favicon('tests/data/favicon2.png', 'custom')

    with mock.patch.object(app, 'url_for') as mock_url_for:
        with app.test_request_context('/') as ctx:
            app.preprocess_request()

            mock_url_for.return_value = 'an/url/'

            assert favicon_url_for('default16x16.png') == 'an/url/'
            mock_url_for.assert_called_with(
                'flask-favicon.static',
                _anchor=None, _method=None, _scheme=None, _external=None,
                filename='default/default16x16.png')

    with mock.patch.object(app, 'url_for') as mock_url_for:
        with app.test_request_context('/') as ctx:
            app.preprocess_request()

            g._flask_favicon.active_icon = g._flask_favicon.icon_registry['custom']

            mock_url_for.return_value = 'an/url/'

            assert favicon_url_for('custom16x16.png') == 'an/url/'
            mock_url_for.assert_called_with(
                'flask-favicon.static',
                _anchor=None, _method=None, _scheme=None, _external=None,
                filename='custom/custom16x16.png')
