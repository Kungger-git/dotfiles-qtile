#!/bin/env bash

# This if statement only executes ksuperkey if you have it installed in your system.
# The need for ksuperkey is only necessary if j4-dmenu-desktop does not show up when the super key is pressed.
# If you don't have ksuperkey installed, get it from the aur: "yay -S ksuperkey"
# Enable Super Keys For Menu
if command -v ksuperkey &> /dev/null; then
    ksuperkey -e 'Super_L=Alt_L|F1' &
    ksuperkey -e 'Super_R=Alt_L|F1' &
fi

# set background
bash $HOME/.config/qtile/scripts/.fehbg

# Kill if already running
killall -9 picom sxhkd dunst xfce4-power-manager

# Launch notification daemon
dunst \
-geom "280x50-10+38" -frame_width "1" -font "Source Code Pro Medium 10" \
-lb "#3D3250FF" -lf "#C4C7C5FF" -lfr "#B07190FF" \
-nb "#3D3250FF" -nf "#C4C7C5FF" -nfr "#B07190FF" \
-cb "#2E3440FF" -cf "#BF616AFF" -cfr "#BF616AFF" &

# power manager and picom start
xfce4-power-manager &
picom --config $HOME/.config/qtile/picom.conf &

if [[ ! `pidof xfce-polkit` ]]; then
    /usr/lib/xfce-polkit/xfce-polkit &
fi

# Start udiskie
udiskie &
