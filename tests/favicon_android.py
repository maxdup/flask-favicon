from flask_favicon.groups.favicon_android import FaviconGroupAndroid, ANDROID_TARGET_SIZES


def test_init():
    CONFIG = {'config': 'config'}
    OUTDIR = 'asset/favicon'

    group = FaviconGroupAndroid(CONFIG, OUTDIR)

    assert group.conf == CONFIG
    assert group.outdir == OUTDIR
    assert group.sizes == ANDROID_TARGET_SIZES
    assert group.filenameSchema == 'android-chrome-{}x{}.png'
