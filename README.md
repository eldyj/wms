# wms

tui session selector written in python with toml config

<img src="screenshot.png"/>

## dependencies

* toml
* rich

## config

config file is located in `~/.config/wms/config.toml` (higher priority)
or in `/etc/wmsconfig.toml`<br/>
<br/>

example config:
```toml
shells = ['ksh','ruby']
editors = ['nvim']

[wms]
xorg = ['i3']

[look]
border = 'simple'
[look.colors]
desktop = 'bold green'
```
