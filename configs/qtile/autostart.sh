#!/bin/env bash

# set background
bash $HOME/.config/qtile/.fehbg

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
