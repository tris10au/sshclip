# sshclip
_A tool for sharing the clipboard between two machines using SSH, useful for when using VNC/RDP without native clipboard support._

## Install
`sshclip` is available from Pip and can be installed with `pip3 install sshclip`

It should automatically install all dependencies (paramiko, pyperclip, click, and pyobjc on macOS).

## Build from source
`sshclip` is a Python 3 package and can be built using `pip3 install --develop .` for development purposes. For typical usage, use `pip3 install .`

## Usage
Run sshclip on both the client (typically your laptop/desktop) and the server (typically the machine you are VNCing into) using the following commmands:

`sshclip client user@example.com` (on the client, replacing `user@example.com` with the SSH connection to the server. The SSH keys must be added to your machine)

`sshclip server` on the server

You may want to put `sshclip server &` in your VNC startup file to make sshclip start automatically.
