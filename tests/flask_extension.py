from flask import g
import os

from flask import Flask
from flask_favicon import FlaskFavicon
from unittest.mock import MagicMock
from unittest import mock

from flask_favicon.flask_extension import _make_bp_static_dir
from flask_favicon.flask_favicon_asset import FlaskFaviconAsset
import pytest


@mock.patch('pathlib.Path.mkdir')
def test_init(appFactory):
    app = appFactory()

    with mock.patch('flask_favicon.FlaskFavicon.init_app') as init_app:

        flaskFavicon = FlaskFavicon()
        init_app.assert_not_called()

        flaskFavicon = FlaskFavicon(app)
        init_app.assert_called_with(app)


@mock.patch('pathlib.Path.mkdir')
@mock.patch('flask_favicon.flask_extension._make_bp_static_dir')
@mock.patch('flask.Flask.before_request')
def test_initapp(mock_mkdir, mock_static_mkdir, mock_before_req, appFactory):

    app = appFactory()

    mock_static_mkdir.return_value = 'STATIC_FOLDER'

    flaskFavicon = FlaskFavicon()
    flaskFavicon.init_app(app)

    assert app.config['FAVICON_BUILD_DIR'] == 'assets/favicon/'
    assert app.config['FAVICON_DEFAULT_BACKGROUND_COLOR'] == '#ffffff'
    assert app.config['FAVICON_DEFAULT_THEME_COLOR'] == '#000000'

    assert flaskFavicon._registry == {}

    assert flaskFavicon.configuration['app_name']
    assert flaskFavicon.configuration['app_name'] == app.name

    assert flaskFavicon.configuration['background_color'] == '#ffffff'
    assert flaskFavicon.configuration['theme_color'] == '#000000'

    assert flaskFavicon.configuration['static_dir'] == 'STATIC_FOLDER'

    mock_static_mkdir.assert_called_once_with(app.config['FAVICON_BUILD_DIR'])
    app.before_request.assert_called_once_with(
        flaskFavicon._flask_favicon_before_request)


@mock.patch('pathlib.Path.mkdir')
@mock.patch('flask_favicon.flask_favicon_asset.FlaskFaviconAsset.generate_assets')
def test_register_favicon(mock_generate, mock_mkdir, appFactory):

    app = appFactory()

    flaskFavicon = FlaskFavicon()
    flaskFavicon.init_app(app)

    # invalid file
    with pytest.raises(FileNotFoundError) as exc_info:
        flaskFavicon.register_favicon(
            'tests/data/favicon-missing.png', 'default-missing')
        assert str(
            exc_info.value) == "'tests/data/favicon-missing.png' could not be found"
        mock_generate.assert_not_called()

    # valid file #1
    flaskFavicon.register_favicon(
        'tests/data/favicon1.png', 'default')
    assert len(flaskFavicon._registry) == 1
    result_fav = flaskFavicon._registry['default']
    assert result_fav
    assert result_fav.favicon_name == 'default'
    assert result_fav.favicon_source == 'tests/data/favicon1.png'
    assert result_fav.base_configuration == flaskFavicon.configuration
    assert result_fav.theme_color == flaskFavicon.configuration['theme_color']
    assert result_fav.background_color == flaskFavicon.configuration['background_color']
    mock_generate.assert_called_once()
    mock_generate.reset_mock()

    # valid file #1
    flaskFavicon.register_favicon('tests/data/favicon2.png', 'default-alt',
                                  background_color='#ff00ff', theme_color='#00ff00')
    assert len(flaskFavicon._registry) == 2
    result_fav = flaskFavicon._registry['default-alt']
    assert result_fav
    assert result_fav.favicon_name == 'default-alt'
    assert result_fav.favicon_source == 'tests/data/favicon2.png'
    assert result_fav.base_configuration == flaskFavicon.configuration
    assert result_fav.theme_color == '#00ff00'
    assert result_fav.background_color == '#ff00ff'
    mock_generate.assert_called_once()


@mock.patch('pathlib.Path.mkdir')
@mock.patch('flask_favicon.flask_favicon_asset.FlaskFaviconAsset.generate_assets')
def test__flask_favicon_before_request(mock_generate, mock_mkdir, appFactory):

    app = appFactory()

    flaskFavicon = FlaskFavicon()
    flaskFavicon.init_app(app)

    # No Favicons
    with app.test_request_context('/') as ctx:

        with mock.patch('warnings.warn') as mock_warn:
            assert '_flask_favicon' not in g
            app.preprocess_request()
            assert '_flask_favicon' in g
            assert g._flask_favicon.icon_registry == flaskFavicon._registry

            mock_warn.assert_called_once_with(
                'Warning: The "default" favicon was not registered during '
                'flask-favicon initialization.')

    # With default Favicon

    flaskFavicon.register_favicon(
        'tests/data/favicon1.png', 'default')
    with app.test_request_context('/') as ctx:
        app.preprocess_request()
        assert '_flask_favicon' in g
        assert g._flask_favicon.icon_registry == flaskFavicon._registry
        assert g._flask_favicon.active_icon == flaskFavicon._registry['default']


@mock.patch('pathlib.Path.mkdir')
def test__make_bp_static_dir(mock_mkdir):
    ret_value = _make_bp_static_dir('DIR/ECTORY/')
    assert ret_value == os.path.join(os.getcwd(), 'DIR/ECTORY')
    mock_mkdir.assert_called_with(parents=True, exist_ok=True)
