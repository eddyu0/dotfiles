# dotfiles

Using idea from [holman](https://github.com/holman/dotfiles), [daviwil](https://github.com/daviwil/dotfiles/tree/master) and [zzh8829](https://github.com/zzh8829/dotfiles)

Most of the configuration are specific to Ubuntu 22.04 (Pop_os 22.04).

## Usage

Bootstrap: install `nala`, `stow`, and then sym-links user dotfiles and system dotfiles using `stow`.

The dotfiles are symlinks to the destination following the sub-folder structure. The system dotfiles folder is mapped to `/` while others are mapped to `$HOME`.

```sh
./bootstrap
```

Using scripts in the `packages/` folder to install packages from apt, custom install steps, flatpak, and other sources such as npm and pip. Then runs every `install.sh` script in each folder (currently only vscode extension). Finally runs `post-install` for application specific setups.

```sh
./install
```

The `update` script can be used to update packages that do not provide auto-update/package manger update.

```sh
./update
```

## Other setup

### Auto login with LUKS encryption

credit to JivanP's [answer](https://www.reddit.com/r/pop_os/comments/uhj78q/comment/ix87a2u/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

1. Edit `/etc/crypttab`, adding the option `keyscript=decrypt_keyctl` to the cryptdata config line:

```text
cryptdata UUID=<cryptdata UUID> none luks,keyscript=decrypt_keyctl
```

2. Edit `/etc/pam.d/common-password`, adding the option `use_authtok` to the GNOME keyring line in order to tell GDM Autologin (which includes this file from `/etc/pam.d/gdm-autologin`) to pass the auth token stored in the keyctl key cryptsetup to GNOME keyring:

```text
password optional pam_gnome_keyring.so use_authtok
```

3. Update the initramfs and reboot:

```sh
sudo apt install initramfs-tools
sudo update-initramfs -k all -c
reboot
```

### Disable elementary appcenter on start

credit to marvelggg's [answer](https://www.reddit.com/r/pop_os/comments/rdz3as/comment/ho4u4bq/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)

```sh
mkdir -p ~/.config/autostart
cp /etc/xdg/autostart/io.elementary.appcenter-daemon.desktop ~/.config/autostart/
echo "X-GNOME-Autostart-enabled=false" >> ~/.config/autostart/io.elementary.appcenter-daemon.desktop
```

### Samba server

```sh
$ sudo vi /etc/samba/smb.conf
[Public]
comment = Samba on Ubuntu
path = /home/username/Public
read only = no
browsable = yes
```

```sh
sudo service smbd restart
sudo ufw allow Samba
sudo smbpasswd -a username
```

Show users

```sh
sudo pdbedit -L -v
```

Connect

```sh
smbclient \\\\host\\Public
```

Mount

```sh
mount -t cifs -o username=bob //host/Public /mnt/path
```
