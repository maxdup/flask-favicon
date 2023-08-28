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
        self.favicon_source = favicon_source
        self.favicon_dir = self._make_favicon_dir(
            favicon_name, configuration['static_dir'])
        self.configuration = configuration

        self.background_color = background_color
        if not self.background_color:
            self.background_color = configuration['background_color']

        self.theme_color = theme_color
        if not self.theme_color:
            self.theme_color = configuration['theme_color']

        # Check if compile required
        self._source_checksum = self._sha256sum(self.favicon_source)
        self._built_checksum = self._compiledsum(self.favicon_dir)

        self.up_to_date = self._source_checksum == self._built_checksum

    def generate_assets(self):
        from PIL import Image

        favicon = Image.open(self.favicon_source)

        favicon_groups = [FaviconGroupStandard, FaviconGroupAndroid,
                          FaviconGroupMS, FaviconGroupApple,
                          FaviconGroupAppleStartup, FaviconGroupYandex]

        for group in favicon_groups:
            group(self.configuration, self.favicon_dir).generate(favicon)

        self.compile_favicon_checksum(self._source_checksum, self.favicon_dir)

    def compile_favicon_checksum(self, checksum, favicon_dir):
        checksum_path = os.path.join(self.favicon_dir, 'checksum')
        with open(checksum_path, 'w') as f:
            f.write(checksum)

    def _make_favicon_dir(self, favicon_name, static_dir):
        favicon_dir = os.path.join(static_dir, favicon_name)
        Path(favicon_dir).mkdir(parents=True, exist_ok=True)
        return favicon_dir

    def _compiledsum(self, favicon_dir):
        try:
            with open(os.path.join(favicon_dir, 'checksum.txt'), 'r') as f:
                compiled_checksum = f.read(64)
                return compiled_checksum
        except:
            return None

    def _sha256sum(self, filename):
        h = hashlib.sha256()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()
