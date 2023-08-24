import os
from PIL import Image


def _hex_color_to_tuple(hex_string):
    return tuple(int(hex_string.strip('#')[i:i+2], 16) for i in (0, 2, 4))


class AbstractFaviconGroup(object):
    def __init__(self, conf, outdir):
        self.conf = conf
        self.outdir = outdir
        self.sizes = []
        self.filenameSchema = '{}x{}.png'

    def generate(self, favicon):
        self.generate_images(favicon)
        self.generate_extras()

    def generate_images(self, favicon):
        for target_size in self.sizes:
            self.generate_image(favicon, size=target_size,
                                image_format='png')

    def generate_image(self, favicon, size=(16, 16), image_format='png',
                       use_background=False, factor=0.9, filename=None):
        filename = filename or self.filenameSchema.format(*size)
        out_path = os.path.join(self.outdir, filename)

        in_ratio = favicon.width/favicon.height
        out_ratio = size[0]/size[1]

        if in_ratio == out_ratio and \
           factor == 1 and \
           not use_background:
            # fast implementation for 1:1 aspect ratios
            favicon_resized = favicon.resize(size)
        else:
            # slower implementation for N:N aspect ratios
            if in_ratio < out_ratio:
                # use height, scale width
                scaled_size = (round(size[0] * factor / out_ratio),
                               round(size[1] * factor))
            else:
                # use width, scale height
                scaled_size = (round(size[0] * factor),
                               round(size[1] * factor * out_ratio))

            favicon = favicon.resize(scaled_size).convert('RGBA')

            x_offset = (size[0] - favicon.width) // 2
            y_offset = (size[1] - favicon.height) // 2

            mode = 'RGBA'
            bg_color = (255, 255, 255, 0)
            mask = None

            if use_background:
                mode = 'RGBA'
                bg_color = _hex_color_to_tuple(self.conf['background_color'])

            favicon_resized = Image.new(mode, size, bg_color)
            favicon_resized.paste(favicon, (x_offset, y_offset), favicon)

        favicon_resized.save(out_path, image_format)

    def generate_extras(self):
        pass
