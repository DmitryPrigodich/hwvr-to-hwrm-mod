"""Convert source Unity material channels to the official HODOR source-map layout."""

import json
import math
from pathlib import Path

from PIL import Image, ImageChops


def transfer(folder: Path, mesh: str):
    material = json.loads((folder/"material-source.json").read_text(encoding="utf-8"))
    properties = material["m_SavedProperties"]
    floats = dict(properties.get("m_Floats", []))
    integers = dict(properties.get("m_Ints", []))
    team_mask = bool(integers.get("_Base_Alpha_As_Color_Mask", 0)
                     or "_BASE_ALPHA_AS_COLOR_MASK_ON" in material.get("m_ValidKeywords", []))
    base = Image.open(folder/f"T_{mesh}_BC.png").convert("RGBA")
    packed = Image.open(folder/f"T_{mesh}_MSEE.png").convert("RGBA")
    normal = Image.open(folder/f"T_{mesh}_N.png").convert("RGBA")
    if len({base.size,packed.size,normal.size}) != 1:
        raise ValueError(f"Texture resolutions disagree: {mesh}")
    # Unity's RG-or-AG decoding covers both BC5 and DXT5nm normal-map layouts.
    red = ImageChops.multiply(normal.getchannel("R"),normal.getchannel("A"))
    green = normal.getchannel("G")
    z_lut = bytes(round(127.5*(1+math.sqrt(max(0,1-(x/127.5-1)**2-(y/127.5-1)**2))))
                  for x in range(256) for y in range(256))
    blue = Image.frombytes("L",base.size,bytes(z_lut[(x<<8)|y]
                           for x,y in zip(red.tobytes(),green.tobytes())))
    prefix = "vr_"+mesh.lower()
    Image.merge("RGB",(red,green,blue)).save(folder/f"{prefix}_NORM.tga")
    metallic, smoothness, emission, secondary = packed.split()
    smooth_factor = floats.get("_Smoothness",1.0)
    metal_factor = floats.get("_Metalness",1.0)
    emission_factor = floats.get("_EmissionBlue",1.0)
    secondary_factor = floats.get("_EmissionAlpha",0.0)
    specular = smoothness.point(lambda x: max(0,min(255,round(x*smooth_factor))))
    reflection = metallic.point(lambda x: max(0,min(255,round(x*metal_factor))))
    glow = ImageChops.add(emission.point(lambda x: max(0,min(255,round(x*emission_factor)))),
                         secondary.point(lambda x: max(0,min(255,round(x*secondary_factor)))))
    for name, channel in (("SPEC",specular),("REFL",reflection),("GLOW",glow)):
        Image.merge("RGB",(channel,)*3).save(folder/f"{prefix}_{name}.tga")
    # An unpainted surface must not accidentally gain the entire alpha as team paint.
    team_on = bool(integers.get("_TeamColorOn", floats.get("_TeamColorOn", 1)))
    mask = base.getchannel("A") if team_mask and team_on else Image.new("L",base.size,0)
    Image.merge("RGB",(mask,)*3).save(folder/f"{prefix}_TEAM.tga")
    report = {"source_material":material["m_Name"],"resolution":list(base.size),
              "normal":"Unity RG-or-AG -> RGB, reconstructed Z", "team_mask_enabled":team_mask and team_on,
              "texture_prefix": prefix,
              "smoothness_factor":smooth_factor,"metalness_factor":metal_factor,
              "emission_factor":emission_factor,"secondary_emission_factor":secondary_factor,
              "mapping":"MSEE.G -> SPEC, MSEE.R -> REFL, MSEE.B/A -> GLOW",
              "shader_conversion":"Approximate conversion from Unity material to HWRM lighting"}
    (folder/"material-transfer.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(f"MATERIAL_OK {mesh}: {base.width}x{base.height}, mask={team_mask}")
    return report
