import random
from user import Admin, SuperUser, RegularUser
from dateutil.relativedelta import *
from datetime import date, datetime

# available user rights
USER_RIGHTS = ["User", "Admin", "Super-User"]

class UserManager:
    """
    Stores the User objects and handles adding or removing them
    """
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)
        print(f"User {user.username} added")

    def remove_user(self, username):
        self.users = [user for user in self.users if user.username != username]
        print(f"User {username} removed.")

    def display_all_users(self):
        for user in self.users:
            user.display_info()

    def user_list(self):
        """
        Makes a list of user dictionaries
        :return: List of dictionaries containing user information
        """
        res = []
        for user in self.users:
            res.append(user.to_dict())
        return res

    def check_duplicate_user(self, username):
        """
        Checks the user list to make sure that the new user being added
        is not there yet
        :param username: username to be added to the list
        :return:
        """
        for u in self.users:
            if u.username == username:
                return True
        return False


def get_user_right_level():
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


def validate_birthday(input_str):
    """
    Checks if the birthdate user submitted was valid
    :param input_str: birthday
    :return: True if valid
    """
    split = input_str.split('/')

    if len(split) != 3:
        return False

    day = split[0]
    month = split[1]
    year = split[2]

    if len(day) != 2:
        return False
    if len(month) != 2:
        return False
    if len(year) != 4:
        return False

    return True


def calculate_age(birthday: datetime):
    """
    Calculates the age of the user
    :param birthday:
    :return: integer value of the age
    """
    today = date.today()
    age = relativedelta(today, birthday)
    return age.years

def ask_birthdate():
    """
    Gets the user's birthday
    :return:
    """
    b_day_format = "dd/mm/yyyy"
    birthday = input(f"Write your birthday in the format {b_day_format}: ")
    while not validate_birthday(birthday):
        birthday = input(f"Please enter a valid birthday in format {b_day_format}: ")
    return datetime.strptime(birthday, "%d/%m/%Y")

def ask_user_details(user_manager: UserManager):
    """
    Asks user for the details of the user account
    :param user_manager:
    :return: User object
    """
    name = input("Enter first name: ")
    lastname = input("Enter last name: ")
    birthdate = ask_birthdate()
    email = input("Enter email: ")
    username = lastname[:3] + name

    while user_manager.check_duplicate_user(username):
        username = input("Duplicate user detected. Please enter new username")

    rights = get_user_right_level()
    password = generate_password()
    if rights == "Admin":
        user = Admin(username, email, " ".join([name, lastname]), password, birthdate)
    elif rights == "Super-User":
        user = SuperUser(username, email, " ".join([name, lastname]), password, birthdate)
    else:
        user = RegularUser(username, email, " ".join([name, lastname]), password, birthdate)
    return user