from twitter import Twitter


def help_text():
    print("Commands include:")
    print("\t help")
    print("\t run")
    print("\t view")


def view_text():
    print("view")


def run_text():
    Twitter()
    return False


def exit_text():
    print("exiting")
    return True


main_menu_switch = {
    "help": help_text,
    "view": view_text,
    "run": run_text,
    "exit": exit_text}


def main_menu(input):
    func = main_menu_switch.get(input, lambda: "Invalid")
    return func()