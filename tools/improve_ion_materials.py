"""Recover Unity packed material channels as HODOR source maps for the ion frigate."""

from pathlib import Path

from transfer_materials import transfer


def prepare():
    return transfer(Path("exports/kus_ioncannonfrigate"),"Kus_IonCannonFrigate")


if __name__ == "__main__":
    prepare()
