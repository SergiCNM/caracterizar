# Script to convert wafermap .py files to .toml
# Usage: python tools/convert_wafermaps.py
import os
import sys
import toml

# Add project root to path so we can import modules if needed
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

wafermaps_dir = os.path.join(project_root, "config", "default", "wafermaps")


def convert_py_to_toml(py_path):
    namespace = {}
    with open(py_path, "r", encoding="utf-8") as f:
        exec(f.read(), namespace)

    if "wafer_parameters" not in namespace:
        print(f"  SKIP: no wafer_parameters in {os.path.basename(py_path)}")
        return None

    return namespace["wafer_parameters"]


def get_toml_name(py_filename):
    base = py_filename.replace(".py", "")
    if not base.endswith("_wafermap"):
        base = base + "_wafermap"
    return base + ".toml"


def main():
    if not os.path.isdir(wafermaps_dir):
        print(f"Directory not found: {wafermaps_dir}")
        sys.exit(1)

    py_files = [f for f in os.listdir(wafermaps_dir) if f.endswith(".py")]
    print(f"Found {len(py_files)} .py files in {wafermaps_dir}\n")

    converted = 0
    errors = 0

    for py_file in sorted(py_files):
        py_path = os.path.join(wafermaps_dir, py_file)
        toml_name = get_toml_name(py_file)
        toml_path = os.path.join(wafermaps_dir, toml_name)

        print(f"Converting: {py_file} -> {toml_name}")
        try:
            wafer_data = convert_py_to_toml(py_path)
            if wafer_data is None:
                errors += 1
                continue

            with open(toml_path, "w", encoding="utf-8") as f:
                toml.dump(wafer_data, f)

            # verify round-trip
            with open(toml_path, "r", encoding="utf-8") as f:
                loaded = toml.load(f)

            # compare keys
            missing = set(wafer_data.keys()) - set(loaded.keys())
            if missing:
                print(f"  WARNING: keys missing after round-trip: {missing}")

            converted += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1

    print(f"\nDone: {converted} converted, {errors} errors")


if __name__ == "__main__":
    main()
