from pam import authenticate as auth
from os import environ
from subprocess import run as sh_exec
from rich import print
from rich.prompt import Prompt as prompt

input = prompt.ask
user = environ['USER']

def valid_pas(pas):
    return auth(user, pas)

def non_crashing_input(text='',**ksargs):
    try:
        return input(text)
    except:
        print('')
        return non_crashing_input(text)

def ask_pas(clear_at_start=True,check_exit=True):
    if clear_at_start:
        sh_exec(['clear'])

    print(f"[green]enter password for {user}[/]")
    pas = non_crashing_input(password=True)

    if check_exit:
        if pas == 'cancel':
            return False

    while not valid_pas(pas):
        print('[red]wrong password[/]')
        pas = non_crashing_input(password=True)
        if check_exit:
            if pas == 'cancel':
                return False

    sh_exec(['clear'])
    return True
