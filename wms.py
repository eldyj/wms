#!/usr/bin/python
from os import environ
from os.path import exists, dirname, abspath
from subprocess import run as sh_exec
from toml import loads as parse_toml
from rich import print, box
from rich.prompt import Prompt as prompt, Confirm as confirm
from rich.markdown import Markdown as md
from rich.table import Table as tab
from rich.align import Align as align
from rich import box
from askpas import ask_pas as input_password

input = prompt.ask
ask = confirm.ask

class Tmp:
    options_count = 0
    options_map = {}
    numbers_map = {}
    options = 0
    shells = []
    locked = []

# this things will just checked, if you don't have something it will ignore it
class Config:
    xorg = ['i3','dwm','xmonad','awesome','bspwm','hypr','wtfwm','leftwm','icewm','openbox']
    wayland = ['sway','Hyprland','qtile']
    shells = ['nu','sh','ash','csh','ksh','ion','zsh','bash','fish','tcsh']
    editors = ['nvim','lvim','vim','nano','micro','hx','emacs']
# look and other
    colors = {
        'desktop':'green',
        'shell':'blue',
        'editor':'magenta',
        'other':'red',
        'option':'yellow',
        'column':'dim',
    }

    password_required = True
    show_suspend = True
    border = 'rounded'
    align = 'left'
    width = 60

Borders = {'rounded':box.ROUNDED,'minimal':box.MINIMAL,'simple':box.SIMPLE,'ascii':box.ASCII}

def init_table():
    if Tmp.options_count != 0:
        Tmp.options_map.clear()
        Tmp.options_count = 0
        Tmp.numbers_map.clear()
        Tmp.shells.clear()
        Tmp.locked.clear()

    Tmp.options = tab(title=f"Hello, {environ['USER']}",width=Config.width,box=Borders.get(Config.border))

    for i in ['#','name','type']:
        Tmp.options.add_column(f"[{Config.colors['column']}]{i}[/]")

def load_config():
    file1 = f"{environ['HOME']}/.config/wms/config.toml"
    file2 = f"/etc/wmsconfig.toml"

    if exists(file1):
        file = file1
    elif exists(file2):
        file = file2
    else:
        return
    
    with open(file) as f:
        tmp = parse_toml(f.read())

    Config.xorg.clear()
    Config.wayland.clear()
    Config.shells.clear()
    Config.editors.clear()
    Config.show_suspend = False
    Config.border = False
   
    if 'security' in tmp:
        if 'password_required' in tmp['security']:
            Config.password_required = tmp['security']['password_required']

    if 'sessions' in tmp:
        if 'wms' in tmp['sessions']:
            if 'wayland' in tmp['sessions']['wms']:
                Config.wayland = tmp['sessions']['wms']['wayland']
            if 'xorg' in tmp['sessions']['wms']:
                Config.xorg = tmp['sessions']['wms']['xorg']

        if 'shells' in tmp['sessions']:
            Config.shells = tmp['sessions']['shells']

        if 'editors' in tmp['sessions']:
            Config.editors = tmp['sessions']['editors']

    if 'look' in tmp:
        if 'align' in tmp['look']:
            Config.align = tmp['look']['align']
        if 'width' in tmp['look']:
            Config.width = tmp['look']['width']
        if 'show_suspend' in tmp['look']:
            Config.show_suspend = tmp['look']['show_suspend']
        if 'border' in tmp['look']:
            Config.border = tmp['look']['border']
        if 'colors' in tmp['look']:
            for i in list(Config.colors):
                if i in tmp['look']['colors']:
                    Config.colors[i] = tmp['look']['colors'][i] 


def add_option(name, command, binary, kind, locked=True):
    try:
        sh_exec(['which',binary],check=True)
    except:
        return

    color = Config.colors['other']
    if kind in {'xorg','wayland'}:
        color = Config.colors['desktop']
    elif kind == 'tty':
        color = Config.colors['shell']
    elif kind == 'editor':
        color = Config.colors['editor']

    if locked:
        Tmp.locked.append(name.split()[0])

    Tmp.options.add_row(f"[{color}]{Tmp.options_count}[/]", f"[{Config.colors['option']}]{name}[/]", f"[{color}]{kind}[/]")
    Tmp.options_map[f"{Tmp.options_count}"] = command
    Tmp.numbers_map[f"{Tmp.options_count}"] = name.split()[0]
    Tmp.options_map[name.split()[0]] = command
    Tmp.options_count += 1

def add_shell(name):
    add_option(f"{name}",[name],name,'tty')
    Tmp.shells.append(name)

def add_xorg(name):
    add_option(f"{name}{'' if 'wm' in name else ' wm'}",['startx',f"/usr/bin/{name}"],name,'xorg')

def add_wayland(name):
    add_option(f"{name}{'' if 'wm' in name else ' wm'}",[name],name,'wayland')

def add_editor(command):
    add_option(command,[command],command,'editor')

def check_options():
    load_config()
    init_table()

    for i in Config.xorg:
        add_xorg(i)

    for i in Config.wayland:
        add_wayland(i)

    for i in Config.shells:
        add_shell(i)

    for i in Config.editors:
        add_editor(i)

    if Config.show_suspend:
        add_option('suspend',['systemctl','suspend'],'systemctl','system')

    add_option('reboot',['reboot','-r','now'],'reboot','system')
    add_option('shutdown',['poweroff','-r','now'],'poweroff','system')

    editor = 'vi' if 'EDITOR' not in environ else environ['EDITOR']
    add_option('edit config',[editor,f"{environ['HOME']}/.config/wms/config.toml"],editor,'wms')
    add_option('cancel',[],'which','wms')

    if 'WMS' in environ:
        Tmp.locked.clear()
        Tmp.locked.append('edit')

    sh_exec(['clear'])

wms_next = f"{dirname(abspath(__file__))}/wms_next"
wms_wm_pid = f"{dirname(abspath(__file__))}/wm_pid"
wms_env = environ.copy()
wms_env['WMS'] = 'true'
wms_env['PWD'] = wms_env['HOME']

def non_crashing_input(**kwargs):
    try:
        return input(**kwargs)
    except:
        print('...')
        return non_crashing_input(**kwargs)

def non_crashing_ask(text):
    try:
        return ask(text)
    except:
        print('')
        return non_crashing_ask(text)

def ask_option():
    option = non_crashing_input(default='0')

    while option not in Tmp.options_map:
        print(f"[red]there is no option with identifier {option}[/red]")
        option = non_crashing_input(default='0')

    return option

def load_wms_script():
    file1 = f"{wms_env['HOME']}/.wms"
    file2 = '/etc/wms'

    if exists(file1):
        file = file1
    elif exists(file2):
        file = file2
    else:
        return

    sh_exec([file],env=wms_env,cwd=wms_env['PWD'])

def main():
    check_options()
    print(align(Tmp.options,align=Config.align))

    if exists(wms_next):
        with open(wms_next,'r') as f:
            choise = f.read()
        sh_exec(['rm',wms_next])
    else:
        choise = ask_option()

    if choise.isnumeric():
        choise = Tmp.numbers_map[choise]

    cmd = Tmp.options_map[choise]

    if Config.password_required:
        if choise in Tmp.locked:
            if not input_password():
                main()
                return

    if choise in ['poweroff','reboot']:
        if non_crashing_ask(f"you really want to {choise}?"):
            sh_exec(cmd)

    if choise == 'cancel':
        if Config.password_required or non_crashing_ask('you really want to exit?'):
            sh_exec(['clear'])
            return

        main()
        return

    if 'WMS' in environ:
        if choise in Config.xorg or choise in Config.wayland or choise in Config.shells:
            with open(wms_next,'w') as f:
                f.write(choise)
            with open(wms_wm_pid) as f:
                sh_exec(['killall',f.read()])
            sh_exec(['clear'])
            return


    wms_env['SHELL'] = choise if choise in Tmp.shells else ""
    sh_exec(['clear'])
    load_wms_script()

    if choise in Config.xorg or choise in Config.wayland or choise in Config.shells:
        with open(wms_wm_pid,'w') as f:
            f.write(choise)

    try:
        p = sh_exec(cmd, env=wms_env, cwd=wms_env['PWD'])
    except:
        pass

    main()

main()
