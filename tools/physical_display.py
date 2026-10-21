"""Keep inspection geometry at physical size at every camera distance."""

import re


def configure(template):
    values=dict(nlips=0,nlipsFar=0,meshRenderLimit=1000000,minimumZoomFactor=.2)
    for field,value in values.items():
        pattern=rf'(?m)^\s*NewShipType\.{field}\s*=[^\n]*'
        line=f'NewShipType.{field}={value}'
        template=re.sub(pattern,line,template) if re.search(pattern,template) else template+'\n'+line
    return template
