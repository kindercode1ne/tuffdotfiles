import os
import re
import xmltodict
from svgwrite import Drawing

def parse_dimension(value: str) -> int:
    if not value:
        return 0
    # Strip common android unit suffixes (dp, dip, sp) and grab leading number
    match = re.search(r'[-+]?\d*\.?\d+', value)
    if not match:
        raise ValueError(f"Cannot parse dimension: {value}")
    return int(round(float(match.group(0))))

def convert_android_color(c: str) -> str:
    if not c:
        return "#000000"
    c = c.strip()
    # Resource reference -> default black (could be enhanced to resolve resources)
    if c.startswith("@"):
        return "#000000"
    # Handle #AARRGGBB
    if re.fullmatch(r'#([0-9a-fA-F]{8})', c):
        aarrggbb = c[1:]
        aa = aarrggbb[0:2]
        rr = aarrggbb[2:4]
        gg = aarrggbb[4:6]
        bb = aarrggbb[6:8]
        if aa.lower() == "ff":
            return f"#{rr}{gg}{bb}"
        # Return rgba with alpha
        alpha = int(aa, 16) / 255.0
        return f"rgba({int(rr,16)},{int(gg,16)},{int(bb,16)},{alpha:.3f})"
    # Already #RRGGBB or similar
    return c

input_dir = "res"  # root folder with all drawable subfolders
output_dir = "svgs"

for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if filename.endswith(".xml"):
            xml_path = os.path.join(root, filename)
            relative_path = os.path.relpath(root, input_dir)
            svg_folder = os.path.join(output_dir, relative_path)
            os.makedirs(svg_folder, exist_ok=True)

            with open(xml_path, "r", encoding="utf-8") as f:
                xml_data = f.read()

            # parse XML
            try:
                data = xmltodict.parse(xml_data)
            except Exception as e:
                print(f"Skip (parse error) {xml_path}: {e}")
                continue
            vector = data.get("vector")
            if not vector:
                continue

            try:
                width = parse_dimension(vector.get("@android:width"))
                height = parse_dimension(vector.get("@android:height"))
            except ValueError as e:
                print(f"Skip (dimension error) {xml_path}: {e}")
                continue

            dwg_path = os.path.join(svg_folder, filename.replace(".xml", ".svg"))
            dwg = Drawing(filename=dwg_path, size=(f"{width}px", f"{height}px"))

            # ViewBox from viewport if present
            try:
                viewport_w = float(vector.get("@android:viewportWidth", width))
                viewport_h = float(vector.get("@android:viewportHeight", height))
                dwg.viewbox(0, 0, viewport_w, viewport_h)
            except Exception:
                dwg.viewbox(0, 0, width, height)

            # Handle <path> elements
            paths = vector.get("path")
            if paths:
                if not isinstance(paths, list):
                    paths = [paths]
                for p in paths:
                    d = p.get("@android:pathData")
                    if not d:
                        continue
                    fill = convert_android_color(p.get("@android:fillColor"))
                    dwg.add(dwg.path(d=d, fill=fill))

            try:
                dwg.save()
            except Exception as e:
                print(f"Failed to save {dwg_path}: {e}")