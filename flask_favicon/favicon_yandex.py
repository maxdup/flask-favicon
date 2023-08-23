import os
import json

from .abstract_favicon_group import AbstractFaviconGroup

YANDEX_TARGET_SIZES = [(50, 50)]


class FaviconGroupYandex(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = YANDEX_TARGET_SIZES
        self.filenameSchema = 'yandex-browser-{}x{}.png'

    def generate_extras(self):
        pass  # TODO yandex-browser-manifest
