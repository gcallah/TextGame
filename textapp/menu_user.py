import text_app as ta


def another_choice():
    print("You made a different choice")
    return True


MY_MENU = {
    ta.TITLE: ta.MAIN_MENU,
    ta.DEFAULT: 0,
    ta.CHOICES: {
        ta.CONTINUE: {ta.FUNC: ta.go_on, ta.TEXT: "Keep running the menu", },
        ta.EXIT: {ta.FUNC: ta.exit, ta.TEXT: "Exit", },
        "2": {ta.FUNC: another_choice, ta.TEXT: "A different choice", },
    },
}


def main():
    ta.run_menu_cont(MY_MENU)


if __name__ == "__main__":
    main()
