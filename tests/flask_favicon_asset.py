import os
import tempfile

from flask_favicon.flask_favicon_asset import FlaskFaviconAsset, _save_sum, _saved_sum, _sha256_sum
from unittest import mock


@mock.patch('flask_favicon.flask_favicon_asset._sha256_sum')
@mock.patch('flask_favicon.flask_favicon_asset._saved_sum')
@mock.patch('pathlib.Path.mkdir')
def test_init(mock_mkdir, mock_saved_sum, mock_sha_sum):

    mock_sha_sum.return_value = '12345'
    mock_saved_sum.return_value = '67890'

    configuration = {
        'static_dir': 'assets/favicon',
        'background_color': '#000000',
        'theme_color': '#ffffff'
    }
    # case #1
    asset = FlaskFaviconAsset(
        'default', 'tests/data/favicon1.png', configuration)

    assert asset.favicon_name == 'default'
    assert asset.favicon_source == 'tests/data/favicon1.png'

    assert asset.favicon_dir == 'assets/favicon/default'
    assert asset.base_configuration == configuration

    assert asset.background_color == '#000000'
    assert asset.theme_color == '#ffffff'

    assert asset._source_checksum == '12345'
    assert asset._saved_checksum == '67890'

    assert asset.up_to_date == False

    # case #2
    mock_saved_sum.return_value = '12345'
    asset = FlaskFaviconAsset(
        'custom-name', 'tests/data/favicon2.png', configuration,
        background_color='#ff0000', theme_color="#00ffff")

    assert asset.favicon_name == 'custom-name'
    assert asset.favicon_source == 'tests/data/favicon2.png'

    assert asset.favicon_dir == 'assets/favicon/custom-name'
    assert asset.base_configuration == configuration

    assert asset.background_color == '#ff0000'
    assert asset.theme_color == '#00ffff'

    assert asset._source_checksum == '12345'
    assert asset._saved_checksum == '12345'

    assert asset.up_to_date == True


def test_generate_assets():
    pass


@mock.patch('flask_favicon.flask_favicon_asset._sha256_sum')
@mock.patch('flask_favicon.flask_favicon_asset._saved_sum')
@mock.patch('flask_favicon.flask_favicon_asset._save_sum')
@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate')
@mock.patch('PIL.Image.open')
def test_generate_assets(mock_image, mock_generate, mock_save_sum, mock_saved_sum, mock_sha_sum):

    mock_sha_sum.return_value = '12345'
    mock_saved_sum.return_value = '67890'

    configuration = {
        'static_dir': 'assets/favicon',
        'background_color': '#000000',
        'theme_color': '#ffffff'
    }
    MOCK_DATA = {'image': True}
    mock_image.return_value = MOCK_DATA

    asset = FlaskFaviconAsset(
        'custom', 'tests/data/favicon1.png', configuration)

    asset.generate_assets()

    mock_image.assert_called_with(asset.favicon_source)
    assert mock_generate.call_count == 6
    mock_generate.assert_called_with(MOCK_DATA)

    mock_save_sum.assert_called_with(
        asset._source_checksum, asset.favicon_dir)


def test__save_sum():
    checksum = '3c19f660f8c1dd90dd940a3359752374f016e8cecdee90a58e1e63b2ca558217'
    with tempfile.TemporaryDirectory() as tmpdirname:
        _save_sum(checksum, tmpdirname)
        checksum_path = os.path.join(tmpdirname, 'checksum.txt')
        assert os.path.exists(checksum_path)

        with open(checksum_path, 'r') as f:
            assert checksum == f.read()


def test__saved_sum():
    checksum = '3c19f660f8c1dd90dd940a3359752374f016e8cecdee90a58e1e63b2ca558217'
    with tempfile.TemporaryDirectory() as tmpdirname:
        checksum_path = os.path.join(tmpdirname, 'checksum.txt')
        with open(checksum_path, 'w') as f:
            f.write(checksum)

        file_checksum = _saved_sum(tmpdirname)
    assert file_checksum == checksum


def test__sha256_sum():
    result = _sha256_sum('tests/data/favicon1.png')
    assert result == '3c19f660f8c1dd90dd940a3359752374f016e8cecdee90a58e1e63b2ca558217'
