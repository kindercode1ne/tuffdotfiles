

import os
import glob
import subprocess

WALLPAPER_DIR = "/home/avery/Wallpapers/"

def main():
    # Get all image files in the wallpaper directory
    images = sorted(glob.glob(os.path.join(WALLPAPER_DIR, "*")))
    if not images:
        print("No wallpapers found.")
        return

    # Build wofi options with icon previews, using null bytes
    entries = []
    for img in images:
        entry = os.path.basename(img).encode('utf-8') + b'\0icon\x1f' + img.encode('utf-8')
        entries.append(entry)
    menu = b'\n'.join(entries)

    # Launch wofi and pass the menu via stdin
    wofi_cmd = [
        "wofi", "-d", "-i", "-p", "Select Wallpaper", "-W", "900", "-H", "600", "-k", "/dev/null"
    ]
    proc = subprocess.Popen(wofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = proc.communicate(menu)
    choice = out.decode('utf-8').strip()
    if not choice:
        return

    # The choice is the basename of the selected image
    selected = os.path.join(WALLPAPER_DIR, choice)
    if not os.path.isfile(selected):
        print("Invalid selection.")
        return

    # Set the wallpaper using swww
    swww_cmd = [
        "swww", "img", selected,
        "--transition-fps", "60",
        "--transition-step", "255",
        "--transition-type", "grow"
    ]
    subprocess.Popen(swww_cmd)

if __name__ == "__main__":
    main()
