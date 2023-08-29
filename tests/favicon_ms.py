from flask_favicon.groups.favicon_ms import FaviconGroupMS, MSTILE_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupMS(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == MSTILE_TARGET_SIZES
    assert group.filenameSchema == 'mstile-{}x{}.png'
