import json
import pandas as pd

from thingspeak import get_data, transform_data
from usermanager import UserManager, ask_user_details


def save_data(parsed_data, filename):
    """
    Saves data in JSON format to the disk
    :param parsed_data: data in json format
    :param filename: name of the file
    :return:
    """
    with open(filename, "w") as file:
        json.dump(parsed_data, file, indent=4)


def show_options(options: dict) -> None:
    """
    Prints out the options for the user
    :param options:
    :return:
    """
    print("Options:")
    # options.items() returns [(1, "First option"), (...)...]
    for key, value in options.items():
        print(f"{key} - {value}")


def run_menu(options: dict) -> int:
    """
    Gets the chosen option from the user
    :param options:
    :return: choice in integer
    """
    is_valid_choice = False
    choice = ""
    while not is_valid_choice:
        show_options(options)
        choice = input("Your choice: ")
        # options.keys() returns a list of integers
        is_valid_choice = choice.isnumeric() and int(choice) in options.keys()
        if not is_valid_choice:
            print("Unknown option!\n")

    choice = int(choice)
    return choice


def visualize_data(data):
    count = int(input("How many records do you want to show? "))
    df = pd.DataFrame(data[:count]) # only shows until the 'count' amount
    print(df)


def add_user(user_manager):
    print(f"{len(user_manager.users)} users in the system: ")
    user_manager.display_all_users()
    user = ask_user_details(user_manager)
    user_manager.add_user(user)


def main():
    """
    Main function of the program
    :return:
    """
    options = {
        1: "Get the movement and temperature data",
        2: "Add user to the system",
        3: "Save data",
        4: "visualize data",
        0: "Exit"
    }
    temperature_motion_data = []
    choice = -1
    user_manager = UserManager()
    while choice != 0:
        choice = run_menu(options)
        if choice == 1:
            raw_data = get_data()
            temperature_motion_data = transform_data(raw_data)
            if temperature_motion_data:
                print("Successfully got the data!")
        elif choice == 2:
            add_user(user_manager)
        elif choice == 3:
            output_file = "data.json"
            output_data = {
                "users": user_manager.user_list(),
                "temperature_motion_data": temperature_motion_data
            }
            save_data(output_data, output_file)
            print(f"Saved data to {output_file}")
        elif choice == 4:
            visualize_data(temperature_motion_data)
    return None

if __name__ == "__main__":
    main()

