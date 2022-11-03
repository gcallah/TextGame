"""
This file defines a simple text menu facility.
"""
import os
# JSON needed for menu data:
import json

import textapp.formatting as fmt

TEST = "test"
PROD = "prod"

SUCCESS = 0
FAILURE = 1
FUNC = "func"
URL = "url"
METHOD = "method"
TEXT = "text"
BAD_CHOICE = -999

DEF_MARKER = "(default)"

TAB = "    "
TITLE = "Title"
DEFAULT = "Default"
CHOICES = "Choices"
MAIN_MENU = "Main Menu"
CONTINUE = "0"
EXIT = "X"
URL0 = "/games/list"
URL1 = "/games/create"
MENUS_DIR = "../menus"

TYPE = "Type"
# types of "screens":
MENU = "Menu"
FORM = "Form"
DATA = "Data"

SUBMIT = "Submit"
RETURN = "Return"

DATA_SET = "Retrieved data"

DATA_TEXT = 0
DATA_URL = 1

PROMPT = "Prompt"
VALUE = "Value"
FLDS = "Fields"
HIVAL = "Hival"
LOWVAL = "Lowval"

# Types of form data:
INT = "INT"
STR = "STR"

TEST_FORM_TITLE = "Test form"

mode = os.getenv("RUN_ENV", PROD)

HAS_TERMCOLOR = True

try:
    from termcolor import colored # noqa
except ImportError:
    HAS_TERMCOLOR = False


def my_input(prompt):
    """
    Mock input if in test!
    """
    global mode
    if mode == TEST:
        return EXIT
    else:
        return input(f"{prompt}: ")


TEST_FORM = {
    TITLE: TEST_FORM_TITLE,
    SUBMIT: {URL: URL0, METHOD: 'post', TEXT: 'Submit'},
    FLDS: {
        "grid_height": {
            VALUE: 20,
            PROMPT: "What is the grid height?",
            TYPE: INT,
            HIVAL: 100,
            LOWVAL: 2
        },
        "grid_width": {
            VALUE: 20,
            PROMPT: "What is the grid width?",
            TYPE: INT,
            HIVAL: 100,
            LOWVAL: 2
        },
    },
}


def build_prompt(fld):
    """
    Builds a prompt for a form fld using data from form description.
    Return the built prompt.
    """
    prompt = f"{fld[PROMPT]} "
    if fld[VALUE]:
        prompt += f"({fld[VALUE]}) "
    if HIVAL in fld and LOWVAL in fld:
        prompt += f"[{fld[LOWVAL]} - {fld[HIVAL]}] "
    return prompt


def get_fld_input(fld):
    prompt = build_prompt(fld)
    return my_input(prompt)


def change_form_fld(fld, val):
    """
    Change a form field if data is valid.
    `val` will come in as a string.
    We will add TYPE == FLOAT later!
    """
    if fld[TYPE] == INT:
        val_ok = False
        while not val_ok:
            try:
                ival = int(val)
                if LOWVAL in fld and HIVAL in fld:  # always need both for now!
                    if ival < fld[LOWVAL] or ival > fld[HIVAL]:
                        print("Value out of range.")
                    else:
                        fld[VALUE] = ival
                        val_ok = True
            except ValueError:
                print("This is an integer field; please enter a number.")
            if not val_ok:
                val = get_fld_input(fld)
    elif fld[TYPE] == STR:
        fld[VALUE] = val


def run_form(form):
    """
    Runs a form and fills in user answers.
    """
    print(fmt.title(form[TITLE]))
    for fld in form[FLDS]:
        answer = get_fld_input(form[FLDS][fld])
        change_form_fld(form[FLDS][fld], answer)
    if form.get(SUBMIT):
        my_input(form[SUBMIT][TEXT])
    return form


TEST_DATA = {
    TYPE: DATA,
    TITLE: DATA_SET,
    DATA: {"Rec1": {"fld0": 0, "fld1": 1}, "Rec2": {"fld0": 2, "fld1": 3}},
    RETURN: "Some URL",
}


def data_repr(data):
    """
    Formats a data object for display.
    """
    ret_url = data.get(RETURN, None)
    data_txt = fmt.title(data[TITLE])
    for i, key in enumerate(data[DATA]):
        data_txt += f"{i}. {key}"
        rec = data[DATA][key]
        for val in rec.values():
            data_txt += f"\t{val}"
        data_txt += "\n"
    return (data_txt, ret_url)


MENU_FILE = f"{MENUS_DIR}/test_menu.json"


def go_on():
    return True


def exit():
    return False


TEST_MENU = {
    TYPE: MENU,
    TITLE: MAIN_MENU,
    DEFAULT: CONTINUE,
    CHOICES: {
        CONTINUE: {FUNC: go_on,
                   TEXT: "Continue displaying menu"},
        EXIT: {FUNC: exit, TEXT: "Exit", },
    },
}


URL_MENU = {
    TYPE: MENU,
    TITLE: MAIN_MENU,
    DEFAULT: CONTINUE,
    CHOICES: {
        "0": {URL: URL0, METHOD: "get", TEXT: "This is some URL", },
        "1": {URL: URL1, METHOD: "get", TEXT: "Some other URL", },
    },
}


FUNC_MAP = {
    "go_on": go_on,
    "exit": exit,
}


def read_menu_file(menu_file, func_map):
    menu = None
    try:
        with open(menu_file, 'r') as f:
            menu = json.load(f)
    except FileNotFoundError:
        print("Could not open menu file:", menu_file)
    return menu


def menu_repr(menu):
    menu_txt = fmt.title(menu[TITLE], True)
    default_choice = f"{menu[DEFAULT]}"
    for key, val in menu[CHOICES].items():
        menu_txt += f"{TAB}{key}. {val[TEXT]}"
        if default_choice == key:
            menu_txt += " " + DEF_MARKER
        menu_txt += "\n"
    menu_txt += f"{fmt.sep()}\n"
    return menu_txt


def menu_repr_colored(menu):
    menu_txt = fmt.title(menu[TITLE], True)
    default_choice = f"{menu[DEFAULT]}"
    for key, val in menu[CHOICES].items():
        colored_key = fmt.menu_choice(key)
        menu_txt += f"{TAB}{colored_key}. {val[TEXT]}"
        if default_choice == key:
            menu_txt += " " + DEF_MARKER
        menu_txt += "\n"
    menu_txt += f"{fmt.sep(True)}\n"
    return menu_txt


def is_valid_choice(choice, menu):
    return choice in menu[CHOICES]


def get_choice(menu):
    c = BAD_CHOICE
    while not is_valid_choice(c, menu):
        try:
            c = my_input("Please enter a choice from the menu above")
            if not c or c.isspace():
                c = menu[DEFAULT]
        except ValueError:
            print("Please enter a number.")
    return c


def get_menu_item(choice, menu):
    return menu[CHOICES][choice]


def exec_choice(choice, menu):
    return get_menu_item(choice, menu)[FUNC]()


def run_menu_once(menu):
    """
    This function runs the menu once, just returning the choice made.
    """
    if (HAS_TERMCOLOR):
        print(menu_repr_colored(menu))
    else:
        print(menu_repr(menu))
    return get_choice(menu)


def get_single_opt(menu):
    """
    Gets the full dict from a menu choice
    """
    return get_menu_item(run_menu_once(menu), menu)


def menu_data_from_file(menu_file, func_map=None):
    """
    Convert a file into in-mem menu.
    We must map the functions' names to strings.
    """
    menu_data = read_menu_file(menu_file, func_map)
    for opt in menu_data:
        if FUNC in opt:
            if func_map is None:
                print("You must provide a function map with your menu.")
                return None
    return menu_data


def run_menu_cont(menu_data):
    """
    This function runs the menu in a loop.
    It will exit when `exec_choice()` returns False.
    """
    result = True
    while result:
        choice = run_menu_once(menu_data)
        result = exec_choice(choice, menu_data)
    return SUCCESS


def main():
    # Running form in test mode needs to be fixed!
    global mode
    ret = data_repr(TEST_DATA)
    print(ret[DATA_TEXT])
    if mode == PROD:
        mod_form = run_form(TEST_FORM)
        # only the field values will go back to the server:
        print(f"The modified form is: {mod_form[FLDS]}")
    return run_menu_cont(TEST_MENU)


if __name__ == "__main__":
    main()
