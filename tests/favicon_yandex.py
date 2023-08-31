import os
import tempfile

from flask_favicon.groups.favicon_yandex import FaviconGroupYandex, YANDEX_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupYandex(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == YANDEX_TARGET_SIZES
    assert group.filename_schema == 'yandex-browser-{}x{}.png'
    assert group.use_background == False
    assert group.scale_factor == 1.0


def test_generate_extras():
    expected_output = '''{
  "version": "0.1.0",
  "api_version": 1,
  "layout": {
    "logo": "yandex-browser-50x50.png",
    "color": "#333333",
    "show_title": true
  }
}'''

    with tempfile.TemporaryDirectory() as tmpdirname:
        CONFIG = {
            'app_name': 'test_app',
            'theme_color': '#111111',
            'background_color': '#333333'
        }
        group = FaviconGroupYandex(CONFIG, tmpdirname)

        group.generate_extras()
        outpath = os.path.join(tmpdirname, 'yandex-browser-manifest.json')
        assert os.path.exists(outpath)
        with open(outpath, 'r') as f:
            text = f.read()
            assert text == expected_output
