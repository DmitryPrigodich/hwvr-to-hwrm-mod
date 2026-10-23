"""Compatibility entry point: build the separate three-layer campaign candidate."""
from build_mod_layers import package

def build():
    return package()

if __name__ == "__main__":
    build()
