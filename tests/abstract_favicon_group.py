from unittest import mock

from flask_favicon.groups.abstract_favicon_group import AbstractFaviconGroup, _hex_color_to_tuple


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = AbstractFaviconGroup(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == []
    assert group.filenameSchema == '{}x{}.png'


@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_image')
@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_images')
@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_extras')
def test_generate(mock_gen_extras, mock_gen_images, mock_gen_image):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    FAVICON = {'fav': 'icon'}

    group = AbstractFaviconGroup(CONFIG, OUTDIR)

    group.generate(FAVICON)
    mock_gen_image.assert_not_called()
    mock_gen_images.assert_called_with(FAVICON)
    mock_gen_extras.assert_called_once()


@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_image')
def test_generate_images(mock_gen_image):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = AbstractFaviconGroup(CONFIG, OUTDIR)
    group.sizes = [(16, 16), (32, 32), (64, 64)]
    FAVICON = {'fav': 'icon'}

    group.generate_images(FAVICON)
    mock_gen_image.assert_has_calls([
        mock.call(FAVICON, size=(16, 16)),
        mock.call(FAVICON, size=(32, 32)),
        mock.call(FAVICON, size=(64, 64)),
    ])


def test_generate_extras():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = AbstractFaviconGroup(CONFIG, OUTDIR)
    group.generate_extras()


def test__hex_color_to_tuple():
    assert _hex_color_to_tuple('#ffffff') == (255, 255, 255)
    assert _hex_color_to_tuple('#ff00ff') == (255, 0, 255)
    assert _hex_color_to_tuple('#808080') == (128, 128, 128)
