from .abstract_favicon_group import AbstractFaviconGroup

APPLE_TARGET_SIZES = [(57, 57), (60, 60), (72, 72), (76, 76), (114, 114),
                      (120, 120), (144, 144), (152, 152), (167, 167),
                      (180, 180), (1024, 1024)]


class FaviconGroupApple(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = APPLE_TARGET_SIZES
        self.filename_schema = 'apple-touch-icon-{}x{}.png'
        self.use_background = True

    def generate_images(self, favicon):

        self.generate_image(favicon, size=(180, 180),
                            filename='apple-touch-icon.png')
        self.generate_image(favicon, size=(180, 180),
                            filename='apple-touch-icon-precomposed.png')

        for target_size in self.sizes:
            self.generate_image(favicon, size=target_size)
