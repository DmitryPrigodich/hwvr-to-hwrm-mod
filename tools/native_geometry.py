"""Read pooled HWRM hull vertices without changing the installed assets.

The decompressor and binary layout are adapted from GuillermoOM/HODEditorJS,
parser/src/{xpress,parse}.rs (CC BY-NC 4.0). Python translation and strict bounds
checks added here. License: third_party/HODEditorJS-LICENSE.txt.
https://github.com/GuillermoOM/HODEditorJS
"""

import struct
from pathlib import Path

from borrow_native_rig import chunks


def decompress(data,size):
    if len(data)==size:return data
    output=bytearray(size);ip=0;op=0;flags=1
    table=((255,2,0,0,1),(65535,2,0,0,2),(65535,6,15,2,2),
           (16777215,8,31,3,3),(255,2,0,0,1),(65535,2,0,0,2),
           (65535,6,15,2,2),(4294967295,11,255,3,4))
    while op<size:
        if flags==1:
            flags=struct.unpack_from('<I',data,ip)[0];ip+=4
            if not flags&0x80000000:raise ValueError('Missing HODOR compression sentinel')
        if flags&1:
            word=int.from_bytes(data[ip:ip+4],'little')
            mask,shift,length_mask,length_shift,used=table[word&7]
            distance=(word&mask)>>shift;length=((word>>length_shift)&length_mask)+3
            ip+=used;length=min(length,size-op)
            if distance>op:raise ValueError('Invalid compressed back reference')
            start=op-distance
            for i in range(length):
                source=start+i
                if 0<distance<4 and i>=3:source-=2+(distance&1)
                output[op]=output[source] if distance else 0;op+=1
        else:
            output[op]=data[ip];op+=1;ip+=1
        flags>>=1
        if ip>len(data):raise ValueError('Truncated compressed pool')
    return bytes(output)


def pools(binary,want_textures=False):
    data=dict(chunks(binary))[b'POOL'];offset=12;result={}
    for name in ('texture','vertex','face'):
        packed,expanded=struct.unpack_from('<II',data,offset);offset+=8
        payload=data[offset:offset+packed];offset+=packed
        if name!='texture' or want_textures:result[name]=decompress(payload,expanded)
    if offset!=len(data):raise ValueError('Unexpected POOL trailing data')
    return result


def mesh_chunks(binary):
    for kind,chunk in chunks(dict(chunks(binary))[b'HVMD'],12):
        if kind!=b'NRML' or chunk[8:12]!=b'MULT':continue
        offset=16;names=[]
        for _ in range(2):
            size=struct.unpack_from('<I',chunk,offset)[0];offset+=4
            names.append(chunk[offset:offset+size].decode('ascii'));offset+=size
        offset+=4
        yield names,chunk,list(chunks(chunk,offset))


def meshes(path):
    binary=Path(path).read_bytes();pool=pools(binary);vo=0;fo=0;result=[]
    for (name,parent),chunk,children in mesh_chunks(binary):
        for kind,child in children:
            if kind!=b'NRML' or child[8:12]!=b'BMSH':continue
            version=struct.unpack_from('>I',child,12)[0]
            lod,count=struct.unpack_from('<ii',child,16);offset=24;parts=[]
            for _ in range(count):
                material,mask,nv,groups,ni=struct.unpack_from('<iIIhI',child,offset);offset+=18
                stride=sum(size for flag,size in ((1,16),(2,16),(4,4),(8,8),(16,8),(32,8),(8192,12),(16384,12))
                           if mask&flag and (flag not in (16,32) or version==1401))
                if not mask&1:raise ValueError('Mesh has no positions')
                pts=[struct.unpack_from('<3f',pool['vertex'],vo+i*stride) for i in range(nv)]
                vo+=nv*stride;fo+=ni*2
                parts.append(dict(material=material,positions=pts,vertices=nv,indices=ni))
            if offset!=len(child):raise ValueError('Unexpected BMSH trailing data')
            result.append(dict(name=name,parent=parent,lod=lod,parts=parts))
    return result
