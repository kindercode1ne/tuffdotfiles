
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


    # Try using --show dmenu --allow-images for image support
    options = "\n".join(f"<img>{img}</img>\n{os.path.basename(img)}" for img in images)
    cmd = f"echo -e '{options}' | wofi --show dmenu --allow-images -i -p 'Select Wallpaper' -W 900 -H 600 -k /dev/null"
    choice = os.popen(cmd).readline().strip()
    if not choice:
        return

    # Extract the filename from the selected entry (should be the last line)
    selected_name = choice.split("\n")[-1]
    selected = os.path.join(WALLPAPER_DIR, selected_name)
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
