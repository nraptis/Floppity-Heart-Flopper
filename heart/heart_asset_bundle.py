# asset_bundle.py
from __future__ import annotations
from pathlib import Path
from typing import Optional

from filesystem.file_utils import FileUtils

from graphics.graphics_texture import GraphicsTexture
from graphics.graphics_sprite import GraphicsSprite
from graphics.graphics_library import GraphicsLibrary

# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_csv/7663343.csv
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_csv/10140238.csv
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_csv/11842146.csv
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_csv/19030958.csv
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_csv/19585145.csv


# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_img/7663343-0001.png
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_img/10140238-0001.png
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_img/11842146-0001.png
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_img/19030958-0001.png
# /Users/naraptis/Desktop/Floppity-Heart-Flopper/data/cardio_img/19585145-0001.png

class HeartAssetBundle:
    
    def __init__(self) -> None:

        self.ekg_image_reference = FileUtils.load_local_pillow_image("/data/cardio_img/", "/7663343-0001")
        
        self.ekg_image_a = FileUtils.load_local_pillow_image("/data/cardio_img/", "10140238-0001")
        self.ekg_image_b = FileUtils.load_local_pillow_image("/data/cardio_img/", "11842146-0001")
        self.ekg_image_c = FileUtils.load_local_pillow_image("/data/cardio_img/", "19030958-0001")
        self.ekg_image_d = FileUtils.load_local_pillow_image("/data/cardio_img/", "19585145-0001")
        self.ekg_image_e = FileUtils.load_local_pillow_image("/data/cardio_img/", "7663343-0001")
        
        self.ekg_texture_original: Optional[GraphicsTexture] = None
        self.ekg_sprite_original: Optional[GraphicsSprite] = None
        
        self.loaded = False

    # ------------------------------------------------------------------
    # Initial load: create texture + sprite instances
    # ------------------------------------------------------------------
    def load(self, graphics: GraphicsLibrary) -> None:

        _ow, _oh = self.ekg_image_reference.size

        self.ekg_texture_original = GraphicsTexture(graphics=graphics)
        self.ekg_texture_original.load_random(width=_ow, height=_oh)

        self.ekg_sprite_original = GraphicsSprite()
        self.ekg_sprite_original.load(self.ekg_texture_original)

        self.ekg_sprite_original.print()


        self.loaded = True

    # ------------------------------------------------------------------
    # Dispose all textures (sprites and dict stay)
    # ------------------------------------------------------------------
    def dispose(self) -> None:
        self.loaded = False

    # ------------------------------------------------------------------
    # Reload: reuse same texture objects, reload GL resources
    # ------------------------------------------------------------------
    def reload(self, graphics: GraphicsLibrary) -> None:
        self.loaded = True
