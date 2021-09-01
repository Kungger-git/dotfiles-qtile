#!/bin/env bash

function run {
    if ! pgrep $1; then
        $@&
    fi
}

# set background
bash $HOME/.fehbg

# starts utility applications at boot time
run xfce4-power-manager &
picom --config $HOME/.config/qtile/picom.conf &

if [[ ! `pidof xfce-polkit` ]]; then
    /usr/lib/xfce-polkit/xfce-polkit &
fi
