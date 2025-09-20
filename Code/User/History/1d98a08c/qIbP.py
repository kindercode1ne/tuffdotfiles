import os
import xmltodict
from svgwrite import Drawing

input_dir = "res/drawable"  # path to your XMLs
output_dir = "svgs"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith(".xml"):
        filepath = os.path.join(input_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            xml_data = f.read()
        
        # parse XML
        data = xmltodict.parse(xml_data)
        vector = data.get("vector")
        if not vector:
            continue
        
        width = int(vector["@android:width"].replace("dp", ""))
        height = int(vector["@android:height"].replace("dp", ""))
        
        dwg = Drawing(filename=os.path.join(output_dir, filename.replace(".xml", ".svg")),
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