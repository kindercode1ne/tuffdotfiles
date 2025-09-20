import os
import xmltodict
from svgwrite import Drawing

input_dir = "icons"  # root folder with all drawable subfolders
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
            data = xmltodict.parse(xml_data)
            vector = data.get("vector")
            if not vector:
                continue

            width = int(vector["@android:width"].replace("dp", ""))
            height = int(vector["@android:height"].replace("dp", ""))

            dwg = Drawing(filename=os.path.join(svg_folder, filename.replace(".xml", ".svg")),
                          size=(width, height))

            # Handle <path> elements
            paths = vector.get("path")
            if paths:
                if not isinstance(paths, list):
                    paths = [paths]
                for p in paths:
                    d = p.get("@android:pathData")
                    fill = p.get("@android:fillColor", "#000000")
                    dwg.add(dwg.path(d=d, fill=fill))

            dwg.save()