from unittest import mock

from flask_favicon.groups.favicon_apple import FaviconGroupApple, APPLE_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupApple(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == APPLE_TARGET_SIZES
    assert group.filename_schema == 'apple-touch-icon-{}x{}.png'
    assert group.use_background == True
    assert group.scale_factor == 1.0


@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_image')
def test_generate_images(mock_gen_image):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = FaviconGroupApple(CONFIG, OUTDIR)
    FAVICON = {'fav': 'icon'}

    group.generate_images(FAVICON)
    expected_calls = [
        mock.call(FAVICON, size=(180, 180),
                  filename='apple-touch-icon.png'),
        mock.call(FAVICON, size=(180, 180),
                  filename='apple-touch-icon-precomposed.png')
    ]
    expected_calls.extend([mock.call(FAVICON, size=size)
                           for size in APPLE_TARGET_SIZES])

    mock_gen_image.assert_has_calls(expected_calls)
