import os
import json

from .abstract_favicon_group import AbstractFaviconGroup

YANDEX_TARGET_SIZES = [(50, 50)]


class FaviconGroupYandex(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = YANDEX_TARGET_SIZES
        self.filename_schema = 'yandex-browser-{}x{}.png'

    def generate_extras(self):
        manifest = {
            'version': '0.1.0',
            'api_version': 1,
            'layout': {
                'logo': self.filename_schema.format(50, 50),
                'color': self.conf.get('background_color'),
                'show_title': True
            }
        }

        manifest_path = os.path.normpath(os.path.join(
            self.outdir, 'yandex-browser-manifest.json'))
        with open(manifest_path, 'w') as f:
            f.write(json.dumps(manifest, indent=2))
