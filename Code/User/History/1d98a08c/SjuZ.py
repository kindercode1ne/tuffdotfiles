import os
import xmltodict
from svgwrite import Drawing

input_dir = "icons"  # root folder with all drawable subfolders
output_dir = "svgs"

for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if not filename.endswith(".xml"):
            continue
        xml_path = os.path.join(root, filename)
        relative_path = os.path.relpath(root, input_dir)
        svg_folder = os.path.join(output_dir, relative_path)
        os.makedirs(svg_folder, exist_ok=True)

        # Read as bytes first; many APK-extracted XMLs are in Android's binary XML format (AAPT2)
        with open(xml_path, "rb") as f:
            raw = f.read()
        try:
            xml_data = raw.decode("utf-8")
        except UnicodeDecodeError:
            # Likely binary AXML (compiled). Inform and skip.
            print(f"Skipping (binary XML not plain text): {xml_path}")
            continue

        # Parse XML safely
        try:
            data = xmltodict.parse(xml_data)
        except Exception as e:
            print(f"Skipping (parse error {e}): {xml_path}")
            continue

        vector = data.get("vector")
        if not vector:
            # Not a vector drawable
            continue

        try:
            width_attr = vector.get("@android:width") or vector.get("@width")
            height_attr = vector.get("@android:height") or vector.get("@height")
            if not width_attr or not height_attr:
                print(f"Skipping (missing width/height): {xml_path}")
                continue
            width = int(width_attr.replace("dp", ""))
            height = int(height_attr.replace("dp", ""))
        except Exception as e:
            print(f"Skipping (bad dimensions {e}): {xml_path}")
            continue

        dwg = Drawing(filename=os.path.join(svg_folder, filename.replace(".xml", ".svg")),
                      size=(width, height))

        # Handle <path> elements (there may be a single dict or a list)
        paths = vector.get("path")
        if paths:
            if not isinstance(paths, list):
                paths = [paths]
            for p in paths:
                d = p.get("@android:pathData") or p.get("@pathData")
                if not d:
                    continue
                fill = p.get("@android:fillColor") or p.get("@fillColor") or "#000000"
                dwg.add(dwg.path(d=d, fill=fill))

        dwg.save()