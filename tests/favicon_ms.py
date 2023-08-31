import os
import tempfile

from flask_favicon.groups.favicon_ms import FaviconGroupMS, MSTILE_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupMS(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == MSTILE_TARGET_SIZES
    assert group.filename_schema == 'mstile-{}x{}.png'
    assert group.use_background == False
    assert group.scale_factor == 1.0


def test_generate_extras():
    expected_output = '''<?xml version="1.0" encoding="UTF-8"?>\n<browserconfig>\n  <msapplication>\n    <tile>\n      <square70x70logo src="mstile-70x70.png"/>\n      <square150x150logo src="mstile-150x150.png"/>\n      <wide310x150logo src="mstile-310x150.png"/>\n      <square310x310logo src="mstile-310x310.png"/>\n      <TileColor>#333333</TileColor>\n    </tile>\n  </msapplication>\n</browserconfig>\n'''

    with tempfile.TemporaryDirectory() as tmpdirname:
        CONFIG = {
            'app_name': 'test_app',
            'theme_color': '#111111',
            'background_color': '#333333'
        }
        group = FaviconGroupMS(CONFIG, tmpdirname)

        group.generate_extras()
        outpath = os.path.join(tmpdirname, 'browserconfig.xml')
        assert os.path.exists(outpath)
        with open(outpath, 'r') as f:
            text = f.read()
            assert text == expected_output
