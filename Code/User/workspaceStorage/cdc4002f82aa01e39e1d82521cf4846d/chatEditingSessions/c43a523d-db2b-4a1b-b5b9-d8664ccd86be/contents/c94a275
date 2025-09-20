
import os
import glob
import subprocess
import random

WALLPAPER_DIR = "/home/avery/Wallpapers/"

def main():
    # Get all image files in the wallpaper directory
    images = sorted(glob.glob(os.path.join(WALLPAPER_DIR, "*")))
    if not images:
        print("No wallpapers found.")
        return

    # Display the list in wofi and get the selected image
    options = "\n".join(os.path.basename(img) for img in images)
    cmd = f"echo -e '{options}' | wofi -d -i -p 'Select Wallpaper' -W 600 -H 400 -k /dev/null"
    choice = os.popen(cmd).readline().strip()
    if not choice:
        return

    # Find the full path of the selected image
    selected = os.path.join(WALLPAPER_DIR, choice)
    if not os.path.isfile(selected):
        print("Invalid selection.")
        return


    # Generate random x and y in [0, 1]
    x = round(random.uniform(0, 1), 3)
    y = round(random.uniform(0, 1), 3)

    # Set the wallpaper using swww with random transition position
    swww_cmd = [
        "swww", "img", selected,
        "--transition-fps", "60",
        "--transition-step", "255",
        "--transition-type", "grow",
        "--transition-pos", f"{x},{y}"
    ]
    subprocess.Popen(swww_cmd)

    # Save the selected wallpaper path for swww.sh
    last_wallpaper_file = os.path.expanduser("~/.config/swww/last_wallpaper.txt")
    try:
        with open(last_wallpaper_file, "w") as f:
            f.write(selected)
    except Exception as e:
        print(f"Failed to save last wallpaper: {e}")

if __name__ == "__main__":
    main()
