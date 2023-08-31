from unittest import mock
from flask_favicon.groups.favicon_standard import FaviconGroupStandard, BROWSER_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupStandard(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == BROWSER_TARGET_SIZES
    assert group.filename_schema == 'favicon-{}x{}.png'
    assert group.use_background == False
    assert group.scale_factor == 1.0


@mock.patch('flask_favicon.groups.abstract_favicon_group.AbstractFaviconGroup.generate_image')
def test_generate_images(mock_gen_image):
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'
    group = FaviconGroupStandard(CONFIG, OUTDIR)
    FAVICON = {'fav': 'icon'}

    group.generate_images(FAVICON)
    expected_calls = [
        mock.call(FAVICON, image_format='ICO', filename='favicon.ico')]
    expected_calls.extend([mock.call(FAVICON, size=size)
                           for size in BROWSER_TARGET_SIZES])

    mock_gen_image.assert_has_calls(expected_calls)
