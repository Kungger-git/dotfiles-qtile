# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401

import os
import subprocess
from libqtile import qtile
from libqtile import bar, layout, widget, hook
from libqtile.widget import base
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
#from libqtile.utils import guess_terminal

# default variables
mod = "mod4"
home_dir = os.path.expanduser("~")
terminal = f"alacritty --config-file {home_dir}/.config/qtile/alacritty/alacritty.yml"

dmenu_conf = "-c -i -l 10 -sb '#3D3250' -sf '#C4C7C5' -fn 'Source Code Pro Medium'"
j4 = f"j4-dmenu-desktop --no-generic --term='{terminal}' --dmenu=\"dmenu -p 'Run Application:' {dmenu_conf}\""

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(f"{terminal} -e fish"), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    #
    # custom keybindings made by me: @KungPaoChick/@Kungger
    #

    # dmenu
    Key(['mod1'], "F1",
        lazy.spawn(j4),
        desc="Launches dmenu desktop applications"
    ),
    Key([mod], "d",
        lazy.spawn(f"dmenu_run -p 'Run Command: ' {dmenu_conf}"),
        desc="Launches dmenu"
    ),
    Key([mod], "n",
        lazy.spawn(f"networkmanager_dmenu {dmenu_conf}"),
        desc="Launches NetworkManager dmenu"
    ),
    Key([mod], "e",
        lazy.spawn("dmedit-configs"),
        desc="Launches Edit Config dmenu"
    ),
    Key([mod], "l",
        lazy.spawn("dmquick-links"),
        desc="Launches Quick Links dmenu"
    ), 

    # Special keys volume control
    Key([], "XF86AudioRaiseVolume", lazy.spawn("volume-up")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("volume-down")),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),

    # no special keys volume control
    #Key([mod], "equal", lazy.spawn("volume-up")),
    #Key([mod], "minus", lazy.spawn("volume-down")),
    #Key([mod], "0", lazy.spawn("amixer set Master toggle")),

    # lock and settings
    Key(["control", "mod1"], "l", lazy.spawn('lock'), desc="Locks Screen"),
    Key(["control", "mod1"], "s", lazy.spawn('xfce4-settings-manager'), desc="Launches Settings"),
    
    # launch applications
    Key([mod, "shift"], "w", lazy.spawn('xdg-open https://start.duckduckgo.com'), desc="Launches Default Web Browser"),
    Key([mod, "shift"], "f", lazy.spawn('thunar'), desc="Launches Pcmanfm File Manager"),
    Key([mod, "shift"], "s", lazy.spawn('spotify'), desc="Launches Spotify"),
    Key([mod, "shift"], "d", lazy.spawn('discord'), desc="Launches Discord"),
    Key([mod, "shift"], "g", lazy.spawn('geany'), desc="Launches Text Editor Geany"),
    Key([mod, "shift"], "c", lazy.spawn('code'), desc="Launches Text Editor Visual Studio Code"),
    Key([mod, "shift"], "o", lazy.spawn('obs'), desc="Launches OBS Studio")
]

# custom workspace names and initialization
class Groupings:

    def init_group_names(self):
        return [("", {"layout": "monadtall"}),     # Terminals
                ("", {"layout": "monadtall"}),     # Web Browser
                ("", {"layout": "monadtall"}),     # File Manager
                ("", {"layout": "monadtall"}),     # Text Editor
                ("", {"layout": "monadtall"}),     # Media
                ("", {"layout": "monadtall"}),     # Music/Audio
                ("漣", {"layout": "monadtall"})]    # Settings

    def init_groups(self):
        return [Group(name, **kwargs) for name, kwargs in group_names]


if __name__ in ["config", "__main__"]:
    group_names = Groupings().init_group_names()
    groups = Groupings().init_groups()

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group


# window layouts
layouts = [
    layout.MonadTall(margin=10, font="Source Code Pro Medium", font_size=10,
                    border_focus="#B07190", border_width=3, border_normal="#2E3440"),
    # layout.Columns(border_focus_stack='#42A5F5'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.Floating(border_focus='#B07190', border_width=3, border_normal="#2E3440"),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Source Code Pro Medium',
    fontsize=12,
    padding=5,
)
extension_defaults = widget_defaults.copy()

# colors for the bar/widgets/panel
def init_colors():
    return [["#3D3250", "#3D3250"], # color 0 
            ["#3D3250", "#3D3250"], # color 1
            ["#C4C7C5", "#C4C7C5"], # color 2
            ["#B07190", "#B07190"], # color 3
            ["#BFBAAC", "#BFBAAC"], # color 4
            ["#3466C2", "#3466C2"], # color 5
            ["#E0B742", "#E0B742"], # color 6
            ["#D56F6E", "#D56F6E"], # color 7
            ["#68CB79", "#68CB79"]] # color 8

colors = init_colors()


def init_widgets_list():
    widgets_list = [
            widget.Spacer(
                length = 2,
                background = colors[1] 
            ),
            
            # Left Side of the bar

            #widget.Image(
            #    filename = "/usr/share/pixmaps/archlinux-logo.png",
            #    background = colors[1],
            #    margin = 3
            #),
            widget.Image(
                filename = "~/.config/qtile/python.png",
                background = colors[1],
                margin = 3,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(
                        j4
                    ),
                    'Button3': lambda : qtile.cmd_spawn(
                        f'{terminal} -e vim {home_dir}/.config/qtile/config.py'
                    )
                }
            ),
            widget.GroupBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                foreground = colors[2],
                background = colors[1],
                borderwidth = 8,
                highlight_method = "text",
                this_current_screen_border = colors[5],
                active = colors[3],
                inactive = colors[4]
            ),
            widget.Sep(
                linewidth = 3,
                margin = 5,
                background = colors[1]
            ),
            widget.Spacer(
                length = 10,
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 12,
                text = "",
                foreground = colors[8],
                background = colors[1]
            ),
            widget.Battery(
                foreground = colors[2],
                background = colors[1],
                format = "{percent:2.0%}"
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "墳",
                foreground = colors[4],
                background = colors[1]
            ),
            widget.Volume(
                foreground = colors[2],
                background = colors[1]
            ),
            #widget.WindowName(
            #    fontsize = 12,
            #    foreground = colors[2],
            #    background = colors[1]
            #),
            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),

            # Center bar

            #widget.PulseVolume(
            #    background = colors[1],
            #    foreground = colors[2],
            #    emoji = True,
            #    fontsize = 12
            #),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "",
                foreground = colors[5],
                background = colors[1]
            ),
            widget.CurrentLayout(
                font = "Source Code Pro Medium",
                fontsize = 12,
                foreground = colors[2],
                background = colors[1] 
            ),
            widget.Sep(
                linewidth = 3,
                background = colors[1] 
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "﬙",
                foreground = colors[6],
                background = colors[1]
            ),
            widget.CPU(
                font = "Source Code Pro Medium",
                format = "{load_percent}%",
                fontsize = 12,
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "",
                foreground = colors[5],
                background = colors[1]
            ),
            widget.Memory(
                font = "Source Code Pro Medium",
                format = "{MemUsed:.0f}{mm}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text= "",
                foreground = colors[7],
                background = colors[1]
            ),
            widget.HDDGraph(
                type = 'box',
                foreground = colors[2],
                background = colors[1],
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"{terminal} -e gtop")
                }
            ),
            widget.Sep(
                linewidth = 3,
                background = colors[1] 
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "",
                foreground = colors[8],
                background = colors[1]
            ),
            # 
            widget.GenPollText(
                foreground = colors[2],
                background = colors[1],
                update_interval = 5,
                func = lambda: subprocess.check_output(f"{home_dir}/.config/qtile/scripts/num-installed-pkgs").decode("utf-8")
            ),

            # Left Side of the bar
            
            widget.Spacer(
                length = bar.STRETCH,
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "",
                foreground = colors[5],
                background = colors[1]
            ),
            widget.Net(
                format = "{down} ↓↑ {up}",
                foreground = colors[2],
                background = colors[1],
                update_interval = 2,
                mouse_callbacks = {
                    'Button1': lambda : qtile.cmd_spawn(f"networkmanager_dmenu {dmenu_conf}")
                }
            ),
            widget.Sep(
                size_percent = 60,
                linewidth = 3,
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "",
                foreground = colors[7],
                background = colors[1]
            ),
            widget.Clock(
                font = "Source Code Pro Medium",
                format = '%b %d-%Y',
                fontsize = 12,
                foreground = colors[2],
                background = colors[1]
            ),
            widget.TextBox(
                font = "Iosevka Nerd Font",
                fontsize = 15,
                text = "",
                foreground = colors[7],
                background = colors[1]
            ),
            widget.Clock(
                font = "Source Code Pro Medium",
                format = '%I:%M:%S %p',
                fontsize = 12,
                foreground = colors[2],
                background = colors[1]
            ),
            widget.Systray(
                background = colors[1] 
            ),
            widget.Spacer(
                length = 5,
                background = colors[1] 
            )
        ]
    return widgets_list


# screens/bar
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_list(), size=30, opacity=0.9, margin=[5,10,0,10]))]

screens = init_screens()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

#
# assign apps to groups/workspace
#
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}

    # assign deez apps
    d[group_names[0][0]] = ['Alacritty', 'xfce4-terminal']
    d[group_names[1][0]] = ['Navigator', 'discord', 'brave-browser', 'midori', 'qutebrowser']
    d[group_names[2][0]] = ['pcmanfm', 'thunar']
    d[group_names[3][0]] = ['code', 'geany']
    d[group_names[4][0]] = ['vlc', 'obs', 'mpv', 'mplayer', 'lxmusic', 'gimp']
    d[group_names[5][0]] = ['spotify']
    d[group_names[6][0]] = ['lxappearance', 'gpartedbin', 'lxtask', 'lxrandr', 'arandr', 'pavucontrol', 'xfce4-settings-manager']

    wm_class = client.window.get_wm_class()[0]
    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen(toggle=False)


main = None
@hook.subscribe.startup
def start_once():
    start_script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.call([start_script])

@hook.subscribe.startup_once
def start_always():
    # fixes the cursor
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
