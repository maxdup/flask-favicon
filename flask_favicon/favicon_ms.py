import os
import json

from .abstract_favicon_group import AbstractFaviconGroup

MSTILE_TARGET_SIZES = [(70, 70), (144, 144), (150, 150),
                       (310, 150), (310, 310)]


class FaviconGroupMS(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = MSTILE_TARGET_SIZES
        self.filenameSchema = 'mstile-{}x{}.png'

    def generate_extras(self):
        pass  # TODO: browserconfig.xml
