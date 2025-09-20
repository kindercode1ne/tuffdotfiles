
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


    # Build wofi options with image previews and names under each
    # Wofi supports images with: <img>path</img> Name (on one line) when --allow-images is used
    options = "\n".join(f"<img>{img}</img> {os.path.basename(img)}" for img in images)
    # Use dmenu mode, image support, and a larger window for previews
    cmd = f"echo -e '{options}' | wofi --show dmenu --allow-images -i -p 'Select Wallpaper' -W 900 -H 600 -k /dev/null"
    choice = os.popen(cmd).readline().strip()
    if not choice:
        return

    # Extract the filename from the selected entry (should be after </img> )
    if '</img>' in choice:
        selected_name = choice.split('</img>')[-1].strip()
    else:
        selected_name = choice.strip()
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
