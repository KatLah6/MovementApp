import random

# available user rights
USER_RIGHTS = ["User", "Admin", "Super-User"]

# This is where we store our users
users_list = []

def query_user_rights():
    print(f"Available right levels: ")
    # print user level selection
    for i, lvl in enumerate(USER_RIGHTS):
        print(f"{i}) {lvl}")
    selection = input("Please select the desired rights level [0 - 2]: ")
    while selection not in ["0", "1", "2"]:
        selection = input("Please select the desired rights level [0 - 2]: ")
    return USER_RIGHTS[int(selection)]

def check_duplicate_user(username):
    global users_list
    for u in users_list:
        if u["username"] == username:
            return True
    return False

def generate_password():
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

def main():
    global users_list # Allows us to access to global variable 'users_list'
    while True:
        print(f"{len(users_list)} users in the system: ")
        for u in users_list:
            print(f"{u["username"]}: {u["rights"]}")
        user = ask_user_details()
        users_list.append(user)
        do_quit = input("Type 'quit' to exit or press enter to add another user: ")
        if do_quit == "quit":
            break


if __name__ == "__main__":
    main()
