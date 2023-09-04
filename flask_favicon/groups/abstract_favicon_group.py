import os


class AbstractFaviconGroup(object):
    def __init__(self, conf, outdir):
        self.conf = conf
        self.outdir = outdir
        self.sizes = []
        self.filename_schema = '{}x{}.png'
        self.scale_factor = 1.0
        self.use_background = False

    def generate(self, favicon):
        self.generate_images(favicon)
        self.generate_extras()

    def generate_images(self, favicon):
        for target_size in self.sizes:
            self.generate_image(favicon, size=target_size)

    def generate_image(self, favicon, size=(16, 16),
                       image_format='png', filename=None):

        filename = filename or self.filename_schema.format(*size)
        out_path = os.path.normpath(os.path.join(self.outdir, filename))

        in_ratio = favicon.width/favicon.height
        out_ratio = size[0]/size[1]

        favicon = favicon.convert('RGBA')

        if abs(in_ratio - out_ratio) < 0.05 and \
           self.scale_factor == 1 and not self.use_background:
            # fast implementation for 1:1 aspect ratios without modifications
            generated_favicon = self._generate_image_simple(
                favicon, size)
        else:
            # slower implementation for N:N aspect ratios
            generated_favicon = self._generate_image_complex(
                favicon, size, in_ratio, out_ratio)

        generated_favicon.save(out_path, image_format)

    def _generate_image_simple(self, favicon, size):
        return favicon.resize(size)

    def _generate_image_complex(self, favicon, size, in_ratio, out_ratio):
        from PIL import Image

        scaled_size_x = size[0] * self.scale_factor
        scaled_size_y = size[1] * self.scale_factor

        if in_ratio < out_ratio:
            # use height, scale width
            scaled_size_x /= out_ratio
        elif in_ratio > out_ratio:
            # use width, scale height
            scaled_size_y *= out_ratio

        scaled_size = (round(scaled_size_x), round(scaled_size_y))

        scaled_favicon = favicon.resize(scaled_size)

        offset = ((size[0] - scaled_size[0]) // 2,
                  (size[1] - scaled_size[1]) // 2)

        bg_color = (255, 255, 255, 0)
        if self.use_background:
            bg_color = _hex_color_to_tuple(self.conf['background_color'])

        out_favicon = Image.new('RGBA', size, bg_color)
        out_favicon.paste(scaled_favicon, offset, scaled_favicon)
        return out_favicon

    def generate_extras(self):
        pass


def _hex_color_to_tuple(hex_string):
    return tuple(int(hex_string.strip('#')[i:i+2], 16) for i in (0, 2, 4))
