"""
This package provides a simple text interface to a GameAPI server.
It relies on the `text_menu` package, which is not yet on PyPi,
"""

import os
from http.client import OK
import requests

from textapp.text_app import get_single_opt, URL, METHOD
from textapp.text_app import TYPE, DATA, data_repr
from textapp.text_app import FORM, run_form, MENU
from textapp.text_app import FLDS, DATA_TEXT

MAIN_MENU_ROUTE = '/main_menu'
MENU_URL = ''

CONTINUE = 1
HALT = 0
ERROR = -1

API_SERVER_URL = "GAME_API_URL"
LOCAL_HOST = "http://127.0.0.1:8000"

EXIT = 'x'


def display_data_page(session, server, data):
    print(f"\n{data_repr(data)[DATA_TEXT]}\n")
    if MENU_URL in data:
        run_menu(session, server, route=data[MENU_URL])


def handle_form(session, server, form):
    form = run_form(form)
    if MENU_URL in form:
        print(f"form[MENU_URL] = {form[MENU_URL]}")
        run_menu(session, server, route=form[MENU_URL])


def run_menu(session, server, route=None, menu=None, form=None):
    """
    The caller must pass *either* `route` OR `menu`.
    """
    print(f"route = {server}{route}")
    status = ERROR
    try:
        if menu is None:
            menu = session.get(f"{server}{route}").json()
            status = menu.status_code
    except Exception as e:
        print(str(e))
    if status != OK:
        return ERROR
    print(f'{menu=}')
    opt = get_single_opt(menu)
    # no URL means exit!
    if not opt.get(URL):
        return HALT

    if opt[METHOD] == 'get':
        result = session.get(f"{server}{opt[URL]}")
        if not result:
            print(f"Get method failed with code: {result.status_code}")
            exit(1)
        print(result.content)
        json_ret = result.json()
        if json_ret[TYPE] == DATA:
            display_data_page(session, server, json_ret)
        elif json_ret[TYPE] == FORM:
            handle_form(session, server, json_ret)
        elif json_ret[TYPE] == MENU:
            run_menu(session, server, menu=json_ret)
    elif opt[METHOD] == 'post':
        if form is None:
            print("Data to post missing from post method.")
            exit(1)
        print(f"Submitting {form[FLDS]}")
        session.post(f"{server}{opt[URL]}")
    return CONTINUE


def main():
    server = os.getenv(API_SERVER_URL, LOCAL_HOST)
    print(f"API server is {server}")
    session = requests.Session()
    cont = CONTINUE
    while cont == CONTINUE:
        cont = run_menu(session, server, route=MAIN_MENU_ROUTE)
    if cont == ERROR:
        return ERROR


if __name__ == "__main__":
    main()
