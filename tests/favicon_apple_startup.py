from unittest import mock

from flask_favicon.groups.favicon_apple_startup import FaviconGroupAppleStartup, APPLE_STARTUP_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupAppleStartup(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == APPLE_STARTUP_SIZES
    assert group.filename_schema == 'apple-touch-startup-image-{}x{}.png'
    assert group.use_background == True
    assert group.scale_factor == 0.33


@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_image')
def test_generate_images(mock_gen_image):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = FaviconGroupAppleStartup(CONFIG, OUTDIR)
    FAVICON = {'fav': 'icon'}

    group.generate_images(FAVICON)
    expected_calls = [mock.call(FAVICON, size=size)
                      for size in APPLE_STARTUP_SIZES]

    mock_gen_image.assert_has_calls(expected_calls)
