from unittest import mock
from PIL import Image

from flask_favicon.groups.abstract_favicon_group import AbstractFaviconGroup, _hex_color_to_tuple


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = AbstractFaviconGroup(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == []
    assert group.filename_schema == '{}x{}.png'
    assert group.use_background == False
    assert group.scale_factor == 1.0


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


@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup._generate_image_simple')
@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup._generate_image_complex')
@mock.patch('PIL.PngImagePlugin.PngImageFile.convert')
@mock.patch('PIL.PngImagePlugin.PngImageFile.save')
def test_generate_image(mock_save, mock_convert, mock_gen_complex, mock_gen_simple):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    favicon = Image.open('tests/data/favicon1.png')

    mock_convert.return_value = favicon
    mock_gen_simple.return_value = favicon
    mock_gen_complex.return_value = favicon

    def reset_mock():
        mock_save.reset_mock()
        mock_convert.reset_mock()
        mock_gen_simple.reset_mock()
        mock_gen_complex.reset_mock()

    group = AbstractFaviconGroup(CONFIG, OUTDIR)

    group.generate_image(favicon)
    mock_convert.assert_called_once_with('RGBA')
    mock_gen_simple.assert_called_with(favicon, (16, 16))
    mock_gen_complex.assert_not_called()
    mock_save.assert_called_once_with('asset/favicon/16x16.png', 'png')

    reset_mock()

    group.generate_image(favicon, size=(64, 32))
    mock_convert.assert_called_once_with('RGBA')
    mock_gen_simple.assert_not_called()
    mock_gen_complex.assert_called_once_with(favicon, (64, 32), 1.0, 2.0)
    mock_save.assert_called_once_with('asset/favicon/64x32.png', 'png')

    reset_mock()

    group.scale_factor = 0.5
    group.generate_image(favicon, size=(32, 32))
    mock_convert.assert_called_once_with('RGBA')
    mock_gen_simple.assert_not_called()
    mock_gen_complex.assert_called_once_with(favicon, (32, 32), 1.0, 1.0)
    mock_save.assert_called_once_with('asset/favicon/32x32.png', 'png')
    reset_mock()

    group.use_background = True
    group.generate_image(favicon, size=(32, 32))
    mock_convert.assert_called_once_with('RGBA')
    mock_gen_simple.assert_not_called()
    mock_gen_complex.assert_called_once_with(favicon, (32, 32), 1.0, 1.0)
    mock_save.assert_called_once_with('asset/favicon/32x32.png', 'png')


@mock.patch('PIL.PngImagePlugin.PngImageFile.resize')
def test__generate_image_simple(mock_resize):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    favicon = Image.open('tests/data/favicon1.png')
    RESIZED = {'output': 'file'}

    mock_resize.return_value = RESIZED

    group = AbstractFaviconGroup(CONFIG, OUTDIR)

    ret = group._generate_image_simple(favicon, (32, 32))
    assert ret == RESIZED
    mock_resize.assert_called_once_with((32, 32))

    mock_resize.reset_mock()

    ret = group._generate_image_simple(favicon, (64, 128))
    assert ret == RESIZED
    mock_resize.assert_called_once_with((64, 128))


@mock.patch('PIL.Image.new')
@mock.patch('PIL.PngImagePlugin.PngImageFile.resize')
def test__generate_image_complex(mock_resize, mock_new):
    CONFIG = {'background_color': '#ff00ff'}
    OUTDIR = 'asset/favicon'
    favicon = Image.open('tests/data/favicon1.png')
    RESIZED = Image.open('tests/data/favicon2.png')
    NEW = Image.new('RGBA', (32, 32), '#ffffff')

    mock_resize.return_value = RESIZED
    mock_new.return_value = NEW

    group = AbstractFaviconGroup(CONFIG, OUTDIR)

    with mock.patch.object(NEW, 'paste', NEW) as mock_paste:

        def mock_resets():
            mock_paste.reset_mock()
            mock_resize.reset_mock()
            mock_new.reset_mock()

        ret = group._generate_image_complex(favicon, (32, 32), 1.0, 1.0)
        assert ret == NEW

        mock_new.assert_called_with('RGBA', (32, 32), (255, 255, 255, 0))
        mock_resize.assert_called_with((32, 32))
        mock_paste.assert_called_once_with(RESIZED, (0, 0), RESIZED)

        mock_resets()

        ret = group._generate_image_complex(favicon, (96, 32), 2.0, 3.0)
        assert ret == NEW

        mock_new.assert_called_with('RGBA', (96, 32), (255, 255, 255, 0))
        mock_resize.assert_called_with((32, 32))
        mock_paste.assert_called_once_with(RESIZED, (32, 0), RESIZED)

        mock_resets()

        group.use_background = True
        ret = group._generate_image_complex(favicon, (32, 64), 4.0, 2.0)
        assert ret == NEW

        mock_new.assert_called_with('RGBA', (32, 64), (255, 0, 255))
        mock_resize.assert_called_with((32, 128))
        mock_paste.assert_called_once_with(RESIZED, (0, -32), RESIZED)

        mock_resets()


def test_generate_extras():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = AbstractFaviconGroup(CONFIG, OUTDIR)
    group.generate_extras()


def test__hex_color_to_tuple():
    assert _hex_color_to_tuple('#ffffff') == (255, 255, 255)
    assert _hex_color_to_tuple('#ff00ff') == (255, 0, 255)
    assert _hex_color_to_tuple('#808080') == (128, 128, 128)
