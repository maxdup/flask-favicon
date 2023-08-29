from flask_favicon.groups.favicon_yandex import FaviconGroupYandex, YANDEX_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupYandex(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == YANDEX_TARGET_SIZES
    assert group.filenameSchema == 'yandex-browser-{}x{}.png'
