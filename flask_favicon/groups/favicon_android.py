import os
import json

from .abstract_favicon_group import AbstractFaviconGroup

ANDROID_TARGET_SIZES = [(36, 36), (48, 48), (72, 72), (96, 96), (144, 144),
                        (192, 192), (256, 256), (384, 384), (512, 512)]


class FaviconGroupAndroid(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = ANDROID_TARGET_SIZES
        self.filename_schema = 'android-chrome-{}x{}.png'

    def generate_extras(self):
        manifest = {
            'name': self.conf.get('app_name'),
            'short_name': self.conf.get('app_name'),
            'description': '',
            'dir': 'auto',
            'lang': 'en-US',
            'display': 'standalone',
            'orientation': 'any',
            'start_url': '.',
            'background_color': self.conf.get('background_color'),
            'theme_color': self.conf.get('theme_color'),
            'icons': []
        }

        for target_size in self.sizes:
            filename = self.filename_schema.format(*target_size)
            manifest['icons'].append({
                'src': filename,
                'sizes': '{}x{}'.format(*target_size),
                'type': 'image/png',
                'purpose': 'any'
            })

        manifest_path = os.path.normpath(
            os.path.join(self.outdir, 'manifest.webmanifest'))
        with open(manifest_path, 'w') as f:
            f.write(json.dumps(manifest, indent=2))
