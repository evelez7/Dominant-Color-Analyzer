import json
from util import main_menu


def main():
    print("welcome to dominant color analyzer")
    exit = False
    while exit is False:
        option = input("Please input command: ")
        exit = main_menu(option)

main()