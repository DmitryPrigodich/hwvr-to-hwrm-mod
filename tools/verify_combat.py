"""Report observed live-engine damage, without treating asset loads as successful combat."""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from prepare_combat_probe import IMPORTED_TEST_SHIPS


def verify(log_path=Path("local/HWRM-test.log")):
    log = log_path.read_text(errors="replace").replace("\0", "")
    combat = log.rsplit("VR_COMBAT: init", 1)[-1]
    result = {"checked_at": datetime.now(timezone.utc).isoformat(),
              "installed_mod_sha256": Path("local/installed-mod-sha256.txt").read_text().strip(),
              "archive_loaded": "VastReachesDemo.big" in log,
              "races": [int(x) for x in re.findall(r"(\d+) Races Discovered", log)],
              "scenario_finished": "VR_COMBAT: complete" in combat,
              "test_script_errors": [s for s in combat.splitlines()
                                     if "stack traceback" in s or "parameter:" in s], "ships": {}}
    for ship in IMPORTED_TEST_SHIPS:
        samples = [float(x) for x in re.findall(
            rf'VR_COMBAT: sample=\d+ ship={ship["id"]} target=([\d.eE+-]+)', combat)]
        result["ships"][ship["id"]] = {
            "loaded": f'VR_COMBAT: loaded {ship["id"]} count=1' in combat,
            "samples": len(samples), "minimum_target_health": min(samples) if samples else None,
            "damage_observed": any(x < 0.999999 for x in samples)}
    result["all_weapons_damage_observed"] = all(s["damage_observed"] for s in result["ships"].values())
    result["complete"] = (result["all_weapons_damage_observed"]
                          and all(s["loaded"] for s in result["ships"].values())
                          and not result["test_script_errors"])
    Path("local/combat-verification.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print("Recent live test output:")
    print("\n".join(combat.splitlines()[-20:]))
    return result


if __name__ == "__main__":
    verify()
