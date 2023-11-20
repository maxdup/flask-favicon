import os
import json

import xml.etree.ElementTree as ET
from xml.dom import minidom

from .abstract_favicon_group import AbstractFaviconGroup

MSTILE_TARGET_SIZES = [(70, 70), (144, 144), (150, 150),
                       (310, 150), (310, 310)]


class FaviconGroupMS(AbstractFaviconGroup):
    def __init__(self, conf, outdir):
        super().__init__(conf, outdir)
        self.sizes = MSTILE_TARGET_SIZES
        self.filename_schema = 'mstile-{}x{}.png'

    def generate_extras(self):

        manifest_path = os.path.normpath(
            os.path.join(self.outdir, 'browserconfig.xml'))
        root = ET.Element('browserconfig')
        msapp = ET.SubElement(root, 'msapplication')
        tile = ET.SubElement(msapp, 'tile')
        ET.SubElement(tile, 'square70x70logo', src='mstile-70x70.png')
        ET.SubElement(tile, 'square150x150logo', src='mstile-150x150.png')
        ET.SubElement(tile, 'wide310x150logo', src='mstile-310x150.png')
        ET.SubElement(tile, 'square310x310logo', src='mstile-310x310.png')
        color = ET.SubElement(tile, 'TileColor')
        color.text = self.conf.get('background_color')

        tree = ET.ElementTree(root)

        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(
            indent='  ', encoding='UTF-8')
        with open(manifest_path, "w") as f:
            f.write(str(xmlstr.decode('UTF-8')))
            f.close()
