import os
import tempfile

from flask_favicon.groups.favicon_android import FaviconGroupAndroid, ANDROID_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupAndroid(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == ANDROID_TARGET_SIZES
    assert group.filename_schema == 'android-chrome-{}x{}.png'
    assert group.use_background == False
    assert group.scale_factor == 1.0


def test_generate_extras():

    expected_output = '''{
  "name": "test_app",
  "short_name": "test_app",
  "description": "",
  "dir": "auto",
  "lang": "en-US",
  "display": "standalone",
  "orientation": "any",
  "start_url": ".",
  "background_color": "#333333",
  "theme_color": "#111111",
  "icons": [
    {
      "src": "android-chrome-36x36.png",
      "sizes": "36x36",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-48x48.png",
      "sizes": "48x48",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-256x256.png",
      "sizes": "256x256",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "android-chrome-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    }
  ]
}'''

    with tempfile.TemporaryDirectory() as tmpdirname:
        CONFIG = {
            'app_name': 'test_app',
            'theme_color': '#111111',
            'background_color': '#333333'
        }
        group = FaviconGroupAndroid(CONFIG, tmpdirname)

        group.generate_extras()

        outpath = os.path.join(tmpdirname, 'manifest.webmanifest')
        assert os.path.exists(outpath)
        with open(outpath, 'r') as f:
            text = f.read()
            assert text == expected_output
