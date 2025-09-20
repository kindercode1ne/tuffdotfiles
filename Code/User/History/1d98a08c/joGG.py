import os
import xmltodict
from svgwrite import Drawing

input_dir = "icons"  # root folder with all drawable subfolders
output_dir = "svgs"

# Helper to robustly read XML with unknown encodings / possible binary junk
def read_xml(path: str):
    with open(path, "rb") as bf:
        raw = bf.read()
    # Try a few common encodings
    for enc in ("utf-8", "utf-16", "iso-8859-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    # Fallback: replace errors so we keep parsable characters
    return raw.decode("utf-8", errors="replace")

for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if not filename.endswith(".xml"):
            continue
        xml_path = os.path.join(root, filename)
        relative_path = os.path.relpath(root, input_dir)
        svg_folder = os.path.join(output_dir, relative_path)
        os.makedirs(svg_folder, exist_ok=True)

        try:
            xml_data = read_xml(xml_path)
        except Exception as e:
            # Skip unreadable files
            print(f"Skipping {xml_path}: cannot read ({e})")
            continue

        try:
            data = xmltodict.parse(xml_data)
        except Exception as e:
            print(f"Skipping {xml_path}: XML parse error ({e})")
            continue

        # xmltodict returns OrderedDict with a single root key; find 'vector'
        vector = data.get("vector")
        if not vector and len(data) == 1:
            # Try to extract sole root element if its name contains 'vector'
            only_root_name, only_root_val = next(iter(data.items()))
            if "vector" in only_root_name.lower():
                vector = only_root_val
        if not vector:
            continue

        # Width/height may appear with android: prefix or without
        width_attr = vector.get("@android:width") or vector.get("@width")
        height_attr = vector.get("@android:height") or vector.get("@height")
        if not width_attr or not height_attr:
            print(f"Skipping {xml_path}: missing width/height")
            continue
        try:
            width = int(str(width_attr).replace("dp", "").strip())
            height = int(str(height_attr).replace("dp", "").strip())
        except ValueError:
            print(f"Skipping {xml_path}: invalid width/height values {width_attr} {height_attr}")
            continue

        dwg = Drawing(filename=os.path.join(svg_folder, filename.replace(".xml", ".svg")),
                      size=(width, height))

        # Handle <path> elements (could be single dict or list)
        paths = vector.get("path")
        if paths and not isinstance(paths, list):
            paths = [paths]
        if paths:
            for p in paths:
                if not isinstance(p, dict):
                    continue
                d = p.get("@android:pathData") or p.get("@pathData")
                if not d:
                    continue
                fill = p.get("@android:fillColor") or p.get("@fillColor") or "#000000"
                dwg.add(dwg.path(d=d, fill=fill))
        else:
            print(f"Warning: no <path> elements in {xml_path}")

        try:
            dwg.save()
        except Exception as e:
            print(f"Failed to save SVG for {xml_path}: {e}")