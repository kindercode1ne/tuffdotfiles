#!/usr/bin/bash
# start swww
LAST_WALLPAPER_FILE="$HOME/.config/swww/last_wallpaper.txt"
if [ -f "$LAST_WALLPAPER_FILE" ]; then
    WALLPAPER=$(cat "$LAST_WALLPAPER_FILE")
    if [ -f "$WALLPAPER" ]; then
        swww img "$WALLPAPER"
    else
        echo "Wallpaper file not found: $WALLPAPER"
    fi
else
    echo "No last wallpaper file found."
fi