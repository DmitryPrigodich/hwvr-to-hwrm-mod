"""Give compiled material records a namespace as well as their texture maps."""

import re
import struct

from borrow_native_rig import chunks, form


def namespace_materials(binary, namespace):
    output=[]
    for kind,chunk in chunks(binary):
        if kind==b'HVMD':
            entries=[]
            for entry_kind,entry in chunks(chunk,12):
                if entry_kind==b'NRML' and entry[8:12]==b'STAT':
                    length=struct.unpack_from('<I',entry,16)[0]
                    old=entry[20:20+length].decode('ascii')
                    if not old.startswith('vrmat_'):
                        name=('vrmat_'+re.sub(r'[^a-z0-9_]','_',namespace.lower())+'_'+old).encode('ascii')
                        body=entry[8:16]+struct.pack('<I',len(name))+name+entry[20+length:]
                        entry=b'NRML'+struct.pack('>I',len(body))+body
                entries.append(entry)
            chunk=form(b'HVMD',b''.join(entries))
        output.append(chunk)
    return b''.join(output)
