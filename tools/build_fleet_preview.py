"""Prepare, verify, package the fleet preview; preserve the original release.

No game launch and no installation. The normal rebuild script restores the
campaign-only source. The preview reuses the established release/install route.
"""
import hashlib
import json
import shutil
from pathlib import Path

import build_minicampaign
from package_minicampaign import package
from prepare_fleet_preview import PROJECT, ROOT, prepare
from verify_fleet_preview import verify
from apply_novokushan_research import apply as apply_research
from verify_novokushan_research import verify as verify_research


def build():
    backup = PROJECT / "local/fleet-preview/baseline-backup"
    marker = backup / "backup.json"
    if backup.exists() and not marker.exists():
        raise RuntimeError("Unrecognised baseline backup folder")
    if not backup.exists():
        backup.mkdir(parents=True)
        release = PROJECT / "local/VastReachesCampaignDemo-release"
        shutil.copytree(release, backup / "VastReachesCampaignDemo-release")
        source = PROJECT / "local/VastReachesMiniCampaign.big"
        shutil.copy2(source, backup / source.name)
        marker.write_text(json.dumps({"identity": "VRC-fleet-preview-baseline-v1",
            "original_archive_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "source": str(release), "game_launched": False}, indent=2) + "\n")
    prepare()
    verify()
    shutil.copy2(PROJECT / "local/fleet-preview/verification.json", PROJECT / "local/fleet-preview/baseline-verification.json")
    apply_research()
    verify_research()
    build_minicampaign.ROOT = ROOT
    speech=PROJECT/'local/campaign-speech/integration.json'
    if speech.exists() and json.loads(speech.read_text(encoding='utf8')).get('enabled') is True:
        import campaign_speech
        build_minicampaign.ROOT=campaign_speech.prepare(seed=ROOT,convert_movies=False)
    build_minicampaign.build()
    package(fleet_preview=True, research=True)


if __name__ == "__main__": build()
