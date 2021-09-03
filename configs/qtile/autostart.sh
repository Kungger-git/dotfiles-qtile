#!/bin/env bash

function run {
    if ! pgrep $1; then
        $@&
    fi
}

# Enable Super Keys For Menu
ksuperkey -e 'Super_L=Alt_L|F1' &
ksuperkey -e 'Super_R=Alt_L|F1' &

# set background
bash $HOME/.fehbg

# Kill if already running
killall -9 picom sxhkd dunst xfce4-power-manager

# Launch notification daemon
run dunst \
-geom "280x50-10+38" -frame_width "1" -font "Source Code Pro Medium 10" \
-lb "#05132DFF" -lf "#C4C7C5FF" -lfr "#42A5F5FF" \
-nb "#05132DFF" -nf "#C4C7C5FF" -nfr "#42A5F5FF" \
-cb "#2E3440FF" -cf "#BF616AFF" -cfr "#BF616AFF" &

# power manager and picom start
run xfce4-power-manager &
picom --config $HOME/.config/qtile/picom.conf &

if [[ ! `pidof xfce-polkit` ]]; then
    /usr/lib/xfce-polkit/xfce-polkit &
fi

# Start udiskie
run udiskie &
