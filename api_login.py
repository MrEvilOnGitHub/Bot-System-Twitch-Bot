import os, pytwitcherapi
from time import sleep

def main():
    a = pytwitcherapi.TwitchSession()
    b = a.get_auth_url()
    a.start_login_server()
    os.system(f'brave "{b}"')
    while not a.authorized:
        sleep(1)
    sleep(2)
    a.shutdown_login_server()
    return a