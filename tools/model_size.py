"""Physical hull bounds and uniform scaling against the installed HWRM hulls."""

import math
import struct
from pathlib import Path

from borrow_native_rig import chunks
from gallery_layout import FACTIONS


def box(points):
    points=list(points)
    return [min(p[a] for p in points) for a in range(3)]+[max(p[a] for p in points) for a in range(3)]


def bounds(path):
    metadata=dict(chunks(dict(chunks(path.read_bytes()))[b'DTRM'],12))
    result=list(struct.unpack_from('<6f',metadata[b'KDOP'],12))
    if not all(math.isfinite(v) for v in result) or any(result[a]>=result[a+3] for a in range(3)):
        raise ValueError('Invalid model bounds: '+str(path))
    return result


def native_path(identifier):
    for root in ('local/hw1ships/ship','local/hw2ships/ship','local/hwrm-base/ship','local/gallery-native/ship'):
        path=Path(root)/identifier/(identifier+'.hod')
        if path.exists():return path
    raise FileNotFoundError('Native comparison hull: '+identifier)


def reference(identifier):
    return next((native for _,groups in FACTIONS for _,pairs in groups for name,native in pairs
                 if name==identifier),None)


def fit(identifier,source_box):
    native=reference(identifier)
    if not native:return 1,None
    target=bounds(native_path(native))
    body={'nku_resourcecollector':'Root_mesh','nku_supportfrigate':'AdvanceSupportFrigate',
          'nku_proximitysensor':'ProximitySensor'}.get(identifier)
    if body:
        from native_geometry import meshes
        geometry=[m for m in meshes(native_path(native)) if m['name']==body and m['lod']==0]
        target=box(p for m in geometry for part in m['parts'] for p in part['positions'])
    dimensions=[target[a+3]-target[a] for a in range(3)]
    axis=max(range(3),key=lambda a:dimensions[a])
    source_axis=max(range(3),key=lambda a:source_box[a+3]-source_box[a])
    factor=dimensions[axis]/(source_box[source_axis+3]-source_box[source_axis])
    # Sub-percent differences are mesh simplification and moving appendages.
    if abs(factor-1)<.005:factor=1
    return factor,dict(native=native,axis='xyz'[axis],source_axis='xyz'[source_axis],factor=factor,
                       source_bounds=source_box,target_bounds=target,
                       native_body_mesh=body,
                       method='Uniform scale by longest hull dimension; articulated native ships use the body mesh')
