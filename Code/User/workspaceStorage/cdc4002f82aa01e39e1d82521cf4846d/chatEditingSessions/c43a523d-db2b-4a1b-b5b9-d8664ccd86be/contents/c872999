
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

    # Build wofi options with icon previews
    options = "\n".join(f"{os.path.basename(img)}\0icon\x1f{img}" for img in images)
    cmd = f"echo -e '{options}' | wofi -d -i -p 'Select Wallpaper' -W 900 -H 600 -k /dev/null"
    choice = os.popen(cmd).readline().strip()
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
