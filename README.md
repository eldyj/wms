# wms

tui session selector written in python with toml config

<img src="screenshot.png"/>

## dependencies

* toml
* rich
* pam (for password\_required)

## show wms after loginning into tty

```sh
# check if you're in tty
if [ "`tty`" = "/dev/tty1" ]; then {
	# this condition needed for ignoring wms in shells opened from wms
	if [ "$WMS" = "" ]; then {
		# change 'wms' to 'python `path to wms.py`' or whatever you have wms
		wms
	}; fi
	return # return needed only for avoiding rest of configs in tty
}; fi
```

## greeting script

this script executes with selected session (before session execution, after selection)<br/>
you can write it in any language, but you need add executable permissions to it (chmod +x ~/.wms)<br/>
it's located in `~/.wms` or `/etc/wms`<br/>

example greeting script with sh:
```sh
#!/bin/sh
echo "Welcome to $SHELL!"
```
same script with python:
```py
#!/usr/bin/python
from os import environ
print(f"Welcome to {environ['SHELL']}!")
```

## config

config file is located in `~/.config/wms/config.toml` (higher priority)
or in `/etc/wmsconfig.toml`<br/>
<br/>

example config:
```toml
[sessions]
shells = ['ksh93','bash','ruby']
editors = ['nvim']

[sessions.wms]
xorg = ['i3','awesome']
wayland = []

[security]
password_required = false

[look]
border = 'rounded'
show_suspend = false

[look.colors]
desktop = 'green'
editor = 'magenta'
shell = 'blue'
other = 'red'
column = 'white'
```
