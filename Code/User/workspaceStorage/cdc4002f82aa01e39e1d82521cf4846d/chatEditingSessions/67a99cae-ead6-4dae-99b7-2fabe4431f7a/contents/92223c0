#!/usr/bin/bash
# start swww with matugen colors

# Source matugen colors (adjust path if needed)
if [ -f "$HOME/.cache/matugen/colors.sh" ]; then
    source "$HOME/.cache/matugen/colors.sh"
fi

WALLPAPERS_DIR=~/Wallpapers/current
WALLPAPER=$(find "$WALLPAPERS_DIR" -type f | shuf -n 1)
swww img "$WALLPAPER"