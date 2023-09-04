from .abstract_favicon_group import AbstractFaviconGroup

APPLE_STARTUP_SIZES = [(640, 1136), (750, 1334), (828, 1792), (1125, 2436),
                       (1136, 640), (1170, 2532), (1242, 2208), (1242, 2688),
                       (1284, 2778), (1334, 750), (1536, 2048),
                       (1620, 2160), (1668, 2224), (1668, 2388), (1792, 828),
                       (2048, 2732), (2048, 2732), (2160, 1620), (2208, 1242),
                       (2224, 1668), (2388, 1668), (2436, 1125), (2532, 1170),
                       (2688, 1242), (2732, 2048), (2778, 1284)]


class FaviconGroupAppleStartup(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = APPLE_STARTUP_SIZES
        self.filename_schema = 'apple-touch-startup-image-{}x{}.png'
        self.scale_factor = 0.33
        self.use_background = True

    def generate_images(self, favicon):
        for target_size in self.sizes:
            self.generate_image(favicon, size=target_size)
