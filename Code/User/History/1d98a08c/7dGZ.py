import os
import re
import xmltodict
from svgwrite import Drawing

def parse_dimension(value: str) -> int:
    if not value:
        return 0
    match = re.search(r'[-+]?\d*\.?\d+', value)
    if not match:
        raise ValueError(f"Cannot parse dimension: {value}")
    return int(round(float(match.group(0))))

def parse_float(value: str, default: float = 0.0) -> float:
    if not value:
        return default
    m = re.search(r'[-+]?\d*\.?\d+', value)
    if not m:
        return default
    try:
        return float(m.group(0))
    except ValueError:
        return default

def parse_color(c: str):
    """
    Returns (hex_color, alpha_float) suitable for SVG (no rgba()).
    If fully transparent, caller can set fill='none'.
    """
    if not c:
        return ("#000000", 1.0)
    c = c.strip()
    if c.startswith("@"):  # unresolved resource
        return ("#000000", 1.0)
    # #AARRGGBB
    if re.fullmatch(r'#([0-9a-fA-F]{8})', c):
        aarrggbb = c[1:]
        aa = int(aarrggbb[0:2], 16)
        rr = aarrggbb[2:4]
        gg = aarrggbb[4:6]
        bb = aarrggbb[6:8]
        alpha = aa / 255.0
        return (f"#{rr}{gg}{bb}", alpha)
    # #RRGGBB (#RGB also allowed by browsers but leave unchanged)
    return (c, 1.0)

input_dir = "res"
output_dir = "svgs2"

for root, _, files in os.walk(input_dir):
    for filename in files:
        if not filename.endswith(".xml"):
            continue

        xml_path = os.path.join(root, filename)
        relative_path = os.path.relpath(root, input_dir)
        svg_folder = os.path.join(output_dir, relative_path)
        os.makedirs(svg_folder, exist_ok=True)

        try:
            with open(xml_path, "r", encoding="utf-8") as f:
                xml_data = f.read()
        except OSError as e:
            print(f"Skip (read error) {xml_path}: {e}")
            continue

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

        # ViewBox
        try:
            viewport_w = float(vector.get("@android:viewportWidth", width))
            viewport_h = float(vector.get("@android:viewportHeight", height))
            dwg.viewbox(0, 0, viewport_w, viewport_h)
        except Exception:
            dwg.viewbox(0, 0, width, height)

        # Paths
        paths = vector.get("path")
        if paths and not isinstance(paths, list):
            paths = [paths]

        if paths:
            for p in paths:
                d = p.get("@android:pathData")
                if not d:
                    continue

                # Fill
                raw_fill = p.get("@android:fillColor")
                fill_color, fill_alpha = parse_color(raw_fill)
                # Optional separate fillAlpha attribute multiplies
                extra_fill_alpha = parse_float(p.get("@android:fillAlpha"), 1.0)
                fill_alpha *= extra_fill_alpha

                # Stroke
                raw_stroke = p.get("@android:strokeColor")
                stroke_color = None
                stroke_alpha = 1.0
                if raw_stroke:
                    stroke_color, stroke_alpha = parse_color(raw_stroke)
                    stroke_alpha *= parse_float(p.get("@android:strokeAlpha"), 1.0)
                    # If stroke alpha ends up 0 treat as no stroke
                    if stroke_alpha == 0.0:
                        stroke_color = None

                stroke_width = None
                if stroke_color:
                    stroke_width = parse_float(p.get("@android:strokeWidth"), 1.0)

                attrs = {}
                if fill_alpha == 0.0 or raw_fill in (None, ""):
                    attrs["fill"] = "none"
                else:
                    attrs["fill"] = fill_color
                    if 0 < fill_alpha < 1:
                        attrs["fill-opacity"] = f"{fill_alpha:.3f}"

                if stroke_color:
                    attrs["stroke"] = stroke_color
                    if stroke_width is not None:
                        attrs["stroke-width"] = stroke_width
                    if 0 < stroke_alpha < 1:
                        attrs["stroke-opacity"] = f"{stroke_alpha:.3f}"

                try:
                    dwg.add(dwg.path(d=d, **attrs))
                except Exception as e:
                    print(f"Skip path in {xml_path}: {e}")

        try:
            dwg.save()
        except Exception as e:
            print(f"Failed to save {dwg_path}: {e}")