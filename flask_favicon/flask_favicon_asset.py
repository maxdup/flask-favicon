import os
import hashlib
from pathlib import Path

from flask_favicon.groups.favicon_ms import FaviconGroupMS
from flask_favicon.groups.favicon_android import FaviconGroupAndroid
from flask_favicon.groups.favicon_standard import FaviconGroupStandard
from flask_favicon.groups.favicon_apple import FaviconGroupApple
from flask_favicon.groups.favicon_apple_startup import FaviconGroupAppleStartup
from flask_favicon.groups.favicon_yandex import FaviconGroupYandex


class FlaskFaviconAsset(object):
    def __init__(self, favicon_name, favicon_source, configuration,
                 background_color=None, theme_color=None):

        self.favicon_name = favicon_name
        self.favicon_source = os.path.normpath(favicon_source)
        self.favicon_dir = os.path.normpath(os.path.join(
            configuration['static_dir'], favicon_name))
        self.base_configuration = configuration

        self.background_color = background_color
        if not self.background_color:
            self.background_color = configuration['background_color']

        self.theme_color = theme_color
        if not self.theme_color:
            self.theme_color = configuration['theme_color']

        # Check if compile required
        self._source_checksum = _sha256_sum(self.favicon_source)
        self._saved_checksum = _saved_sum(self.favicon_dir)

        self.up_to_date = self._source_checksum == self._saved_checksum

    def generate_assets(self):

        from PIL import Image

        favicon = Image.open(self.favicon_source)

        Path(self.favicon_dir).mkdir(parents=True, exist_ok=True)

        favicon_groups = [FaviconGroupStandard, FaviconGroupAndroid,
                          FaviconGroupMS, FaviconGroupApple,
                          FaviconGroupAppleStartup, FaviconGroupYandex]

        for group in favicon_groups:
            group(self.base_configuration, self.favicon_dir).generate(favicon)

        _save_sum(self._source_checksum, self.favicon_dir)


CHECKSUM_FILENAME = 'checksum.txt'


def _save_sum(checksum, favicon_dir):
    checksum_path = os.path.normpath(
        os.path.join(favicon_dir, CHECKSUM_FILENAME))
    with open(checksum_path, 'w') as f:
        f.write(checksum)


def _saved_sum(favicon_dir):
    try:
        with open(os.path.normpath(os.path.join(favicon_dir, CHECKSUM_FILENAME)), 'r') as f:
            compiled_checksum = f.read(64)
            return compiled_checksum
    except:
        return None


def _sha256_sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
