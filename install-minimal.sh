#!/bin/env bash
set -e

set_color() {
    if [ -t 1 ]; then
        RED=$(printf '\033[31m')
        GREEN=$(printf '\033[32m')
        YELLOW=$(printf '\033[33m')
        BLUE=$(printf '\033[34m')
        BOLD=$(printf '\033[1m')
        RESET=$(printf '\033[m')
    else
        RED=""
        GREEN=""
        YELLOW=""
        BLUE=""
        BOLD=""
        RESET=""
    fi
}

main() {
    set_color

    # creates srcs folder
    if [[ ! -d $HOME/.srcs/ ]]; then
	    mkdir -p $HOME/.srcs/
    fi
    
    # replaces pacman.conf
    sudo cp -f systemfiles/pacman.conf /etc/

    # adds insults to sudoers.d
    sudo cp -f systemfiles/01_pw_feedback /etc/sudoers.d/

    reset
    echo "${BLUE}"
    echo "▄▄      ▄▄ ▄▄▄▄▄▄▄▄  ▄▄           ▄▄▄▄     ▄▄▄▄    ▄▄▄  ▄▄▄  ▄▄▄▄▄▄▄▄  ▄▄"; sleep 0.1
    echo "██      ██ ██▀▀▀▀▀▀  ██         ██▀▀▀▀█   ██▀▀██   ███  ███  ██▀▀▀▀▀▀  ██"; sleep 0.1
    echo "▀█▄ ██ ▄█▀ ██        ██        ██▀       ██    ██  ████████  ██        ██"; sleep 0.1
    echo " ██ ██ ██  ███████   ██        ██        ██    ██  ██ ██ ██  ███████   ██"; sleep 0.1
    echo " ███▀▀███  ██        ██        ██▄       ██    ██  ██ ▀▀ ██  ██        ▀▀"; sleep 0.1
    echo " ███  ███  ██▄▄▄▄▄▄  ██▄▄▄▄▄▄   ██▄▄▄▄█   ██▄▄██   ██    ██  ██▄▄▄▄▄▄  ▄▄"; sleep 0.1
    echo " ▀▀▀  ▀▀▀  ▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀     ▀▀▀▀     ▀▀▀▀    ▀▀    ▀▀  ▀▀▀▀▀▀▀▀  ▀▀"
    echo "${RESET}"

    #
    # choose video driver
    #
    echo "${BOLD}##########################################################################${RESET}

${RED}1.) xf86-video-amdgpu     ${GREEN}2.) nvidia     ${BLUE}3.) xf86-video-intel${RESET}     4.) Skip

${BOLD}##########################################################################${RESET}"
    read -r -p "${YELLOW}${BOLD}[!] ${RESET}Choose your video card driver. ${YELLOW}(Default: 1)${RESET}: " vidri
    
    #
    # post prompt process
    #
    #
    
    # video driver card case
    case $vidri in
    [1])
            DRIVER='xf86-video-amdgpu xf86-video-ati xf86-video-fbdev'
            ;;

    [2])
            DRIVER='nvidia nvidia-settings nvidia-utils'
            ;;

    [3])
            DRIVER='xf86-video-intel xf86-video-nouveau'
            ;;

    [4])
            DRIVER="xorg-xinit"
            ;;

    *)
            DRIVER='xf86-video-amdgpu xf86-video-ati xf86-video-fbdev'
            ;;
    esac

    ## full system upgrade
    clear
    printf "${GREEN}${BOLD}[*] ${RESET}Performing System Upgrade and Installation...\n\n"
    sudo pacman -Syu --noconfirm

    # installing selected video driver
    sudo pacman -S --needed --noconfirm $DRIVER

    # installs package dependencies
    sudo pacman -S --needed --noconfirm - < packages.txt

    # installs fish
    if ! command -v fish &> /dev/null; then
	    echo "${GREEN}${BOLD}[*] ${RESET}Installing fish shell..."
	    sudo pacman -S --noconfirm fish

	    # downloads oh-my-fish installer script in .srcs folder
	    curl -L https://get.oh-my.fish/ > $HOME/.srcs/install.fish; chmod +x $HOME/.srcs/install.fish
	    clear
	    echo "${YELLOW}${BOLD}[!] ${RESET}oh-my-fish install script has been downloaded. You can execute the installer later on in ${YELLOW}$HOME/.srcs/install.fish${RESET}"; sleep 3

	    # copies fish configurations
	    if [[ ! -d $HOME/.config/fish/ ]]; then
	        mkdir -p $HOME/.config/fish
            cp -f shells/fish/config.fish $HOME/.config/fish/
        else
            cp -f shells/fish/config.fish $HOME/.config/fish/ 
	    fi
    fi

    # touchpad config
    sudo cp -f systemfiles/02-touchpad-ttc.conf /etc/X11/xorg.conf.d/

    # enable display manager
    sudo systemctl enable lxdm.service

    # generate user directories
    xdg-user-dirs-update

    # lxdm theme
    sudo cp -f lxdm/lxdm.conf /etc/lxdm/
    sudo cp -rf lxdm/lxdm-theme/* /usr/share/lxdm/themes/

    # copies scripts to /usr/local/bin
    sudo cp -f scripts/* /usr/local/bin

    # copies dots to home directory
    cp -f dots/.dmrc      \
          dots/.gtkrc-2.0 \
          dots/.vimrc $HOME

    # copies configurations
    cp -rf configs/* $HOME/.config/

    # replaces username
    sed -i "s/kungger/$USER/g" $HOME/.gtkrc-2.0

    # compiles dmenu
    if [[ ! -d $HOME/.config/dmenu ]]; then
        git clone https://github.com/KungPaoChick/dmenu-kungger.git $HOME/.config/dmenu
        (cd $HOME/.config/dmenu; sudo make install)
    fi

    # installs fonts for bar
    FDIR="$HOME/.local/share/fonts"
    echo -e "\n${GREEN}${BOLD}[*] ${RESET}Installing fonts..."
    if [[ -d "$FDIR" ]]; then
        cp -rf fonts/* "$FDIR"
    else
        mkdir -p "$FDIR"
        cp -rf fonts/* "$FDIR"
    fi

    # final
    clear
    read -p "${GREEN}$USER!${RESET}, Reboot Now? ${YELLOW}(Required)${RESET} [Y/n] " reb
    if [[ "$reb" == "" || "$reb" == "Y" || "$reb" == "y" ]]; then
        sudo reboot now
    else
        printf "\n${RED}Abort!${RESET}\n"
    fi
}

main "@"
