from datetime import datetime
import json
import pandas as pd
import pytz
import random
import requests


URL = "https://api.thingspeak.com/channels/2578404/feeds.json?api_key=XSXF6WH7DAECB6S1&results=20"
FINNISH_TZ = pytz.timezone("Europe/Helsinki")


# available user rights
USER_RIGHTS = ["User", "Admin", "Super-User"]

# This is where we store our users
users_list = []

def query_user_rights():
    """
    Asks the user to choose which right level is for their login
    :return:
    """
    print(f"Available right levels: ")
        # print user level selection
    # enumerate gives this: [(0, "User"), (1, "Admin"), (2, "Super-User")]
    for number, level in enumerate(USER_RIGHTS):
        print(f"{number}) {level}")
    selection = input("Please select the desired rights level [0 - 2]: ")
    while selection not in ["0", "1", "2"]:
        selection = input("Please select the desired rights level [0 - 2]: ")
    return USER_RIGHTS[int(selection)]

def check_duplicate_user(username):
    """
    Checks the user list to make sure that the new user being added
    is not there yet
    :param username: username to be added to the list
    :return:
    """
    global users_list
    for u in users_list:
        if u["username"] == username:
            return True
    return False

def generate_password():
    """
    Generates a random password for the user
    :return:
    """
    # ask the user for the numbers of different category of characters
    # capital letters in ASCII are from number 65 to 90
    # lower case letters in ASCII are from number 97 to 122
    # numbers are from 48 to 57
    # special characters are from 32 to 47, 59 - 64, 91 - 96 and 123 - 126
    # we generate a random number and then we convert it to ASCII character with the knowledge above
    # for example chr(72) converts to 'H'
    user_happy = False
    while not user_happy:
        print("Generating password...")
        nof_capital_letters = int(input("How many capital letters you want? "))
        nof_lower_letters= int(input("How many lower letters you want? "))
        nof_numbers= int(input("How many numbers you want? "))
        nof_special_characters= int(input("How many special characters you want? "))
        capital_letters = []
        for i in range(0, nof_capital_letters):
            capital_letters.append(chr(random.randrange(65, 90)))
        low_letters = []
        for i in range(0, nof_lower_letters):
            low_letters.append(chr(random.randrange(97, 122)))
        numbers = []
        for i in range(0, nof_numbers):
            numbers.append(chr(random.randrange(48,57)))
        special_characters = []
        SPECIAL_RANGES = [
            (32, 47),
            (59, 64),
            (91, 96),
            (123, 126)
        ]
        for i in range(0, nof_special_characters):
            range_index = random.randrange(0, len(SPECIAL_RANGES) - 1)
            special_characters.append(
                chr(random.randrange(
                    SPECIAL_RANGES[range_index][0],
                    SPECIAL_RANGES[range_index][1])
                    ))
        password = "".join(capital_letters) + "".join(numbers) + "".join(low_letters) + "".join(special_characters)
        print(f"Generated password: {password}")
        user_happy_query = input("Are you happy with the password? [y, n] ")
        user_happy = user_happy_query == 'y'
    return password

def ask_user_details():
    """
    Asks user for the user details
    :return: a dictionary containing the user data
    """
    global users_list
    name = input("Enter first name: ")
    lastname = input("Enter last name: ")
    age = int(input("Enter age in number format: "))
    username = lastname[:3] + name

    while check_duplicate_user(username):
        username = input("Duplicate user detected. Please enter new username")

    rights = query_user_rights()
    password = generate_password()
    # Dictionary of a user
    user =  {
        "name": " ".join([name, lastname]),
        "age": age,
        "username": username,
        "rights": rights,
        "password": password
        }
    print (password)
    return user

def convert_to_finnish_time(utc_time_str):
    """
    Converts the incoming time to a finnish time
    :param utc_time_str: Timestamp string
    :return: Finnish timestamp string
    """
    input_format = "%Y-%m-%dT%H:%M:%SZ"
    # Parse the UTC time string to a datetime object
    utc_time = datetime.strptime(utc_time_str, input_format)
    # Set the timezone to UTC
    utc_time = utc_time.replace(tzinfo=pytz.utc)
    # Convert to Finnish time
    finnish_time = utc_time.astimezone(FINNISH_TZ)
    # Format the datetime object to the desired format
    return finnish_time.strftime("%d.%m.%Y, %H:%M")

def get_data(url: str):
    """
    Makes an API call to the supplied URL using HTTP GET method
    :param url:
    :return: Response JSON or None
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def transform_data(raw_data):
    """
    Parses the JSON data into more usable format
    :param raw_data: JSON format data
    :return: parsed data
    """
    res = []
    for entry in raw_data["feeds"]:
        finnish_time = convert_to_finnish_time(entry["created_at"])
        data = {
            "movement": entry["field1"],
            "temperature": entry["field2"],
            "time": finnish_time
        }
        res.append(data)
    return res


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


def add_user(users_list):
    print(f"{len(users_list)} users in the system: ")
    for u in users_list:
        print(f"{u["username"]}: {u["rights"]}")
    user = ask_user_details()
    users_list.append(user)


def main():
    """
    Main function of the program
    :return:
    """
    global users_list  # Allows us to access to global variable 'users_list'
    options = {
        1: "Get the movement and temperature data",
        2: "Add user to the system",
        3: "Save data",
        4: "visualize data",
        0: "Exit"
    }
    temperature_motion_data = []
    choice = -1
    while choice != 0:
        choice = run_menu(options)
        if choice == 1:
            raw_data = get_data(URL)
            temperature_motion_data = transform_data(raw_data)
            if temperature_motion_data:
                print("Successfully got the data!")
        elif choice == 2:
            add_user(users_list)
        elif choice == 3:
            output_file = "data.json"
            output_data = {
                "users": users_list,
                "temperature_motion_data": temperature_motion_data
            }
            save_data(output_data, output_file)
        elif choice == 4:
            visualize_data(temperature_motion_data)
    return None

if __name__ == "__main__":
    main()

