#!/usr/bin/env bash
#start swww
WALLPAPERS_DIR=~/Wallpapers/current
WALLPAPER=$(find "$WALLPAPERS_DIR" -type f | shuf -n 1)
swww img "$WALLPAPER"

# Generate Wofi theme with Matugen
matugen "$WALLPAPER" --type wofi --output ~/.config/wofi/matugen.css

# (Optional) Symlink style.css to matugen.css if not already
if [ ! -L ~/.config/wofi/style.css ]; then
    ln -sf ~/.config/wofi/matugen.css ~/.config/wofi/style.css
fi