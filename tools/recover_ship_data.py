"""Recover original ship configurations and prefab transforms from the Mono demo."""

import argparse
import json
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator


def recover(game: Path, output: Path):
    generator = TypeTreeGenerator("2021.3.38f1")
    generator.load_local_game(str(game))
    env = UnityPy.load(str(game / "HomeworldVastReachesDemo_Data/resources.assets"))
    objects = {obj.path_id: obj for obj in env.objects}
    names = {obj.path_id: obj.peek_name() or "" for obj in env.objects if obj.type.name == "MonoBehaviour"}
    env.typetree_generator = generator
    definitions, failures = {}, []
    for obj in env.objects:
        name = names.get(obj.path_id, "")
        if not name.startswith(("Ship_", "Turret_", "Build_", "Laser_")):
            continue
        try:
            definitions[name] = obj.parse_as_dict()
        except Exception as exc:
            failures.append({"name": name, "error": str(exc)})

    def tree(game_object_id):
        go = objects[game_object_id].parse_as_dict()
        node = {"name": go["m_Name"], "id": game_object_id, "components": []}
        for component in go["m_Component"]:
            obj = objects[component["component"]["m_PathID"]]
            if obj.type.name == "Transform":
                transform = obj.parse_as_dict()
                for key in ("m_LocalPosition", "m_LocalRotation", "m_LocalScale"):
                    node[key] = transform[key]
                node["children"] = [tree(objects[p["m_PathID"]].parse_as_dict()["m_GameObject"]["m_PathID"])
                                    for p in transform["m_Children"]]
            elif obj.type.name in ("MeshFilter", "MonoBehaviour", "MeshRenderer"):
                try:
                    node["components"].append({"type": obj.type.name, "data": obj.parse_as_dict()})
                except Exception as exc:
                    node["components"].append({"type": obj.type.name, "error": str(exc)})
        return node

    prefabs, views = {}, {}
    for name, data in definitions.items():
        if name.startswith("Ship_") and data.get("_meshPrefab", {}).get("m_PathID"):
            try:
                prefabs[name] = tree(data["_meshPrefab"]["m_PathID"])
                view = objects[data["_view"]["m_PathID"]].parse_as_dict()
                views[name] = tree(view["m_GameObject"]["m_PathID"])
            except Exception as exc:
                failures.append({"name": name, "prefab_error": str(exc)})
    output.mkdir(parents=True, exist_ok=True)
    (output / "definitions.json").write_text(json.dumps(definitions, indent=2), encoding="utf-8")
    (output / "prefabs.json").write_text(json.dumps(prefabs, indent=2), encoding="utf-8")
    (output / "views.json").write_text(json.dumps(views, indent=2), encoding="utf-8")
    (output / "failures.json").write_text(json.dumps(failures, indent=2), encoding="utf-8")
    print(f"Recovered {len(definitions)} definitions and {len(prefabs)} prefabs; {len(failures)} failures")
    for name, data in prefabs.items():
        print(name, data["name"], data.get("m_LocalScale"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("game", type=Path)
    parser.add_argument("--output", type=Path, default=Path("local/recovered"))
    args = parser.parse_args()
    recover(args.game, args.output)
