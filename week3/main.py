
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

def generate_password(name, lastname, age):
    return "placeholder"

def ask_user_details():
    global users_list
    name = input("Enter first name: ")
    lastname = input("Enter last name: ")
    age = int(input("Enter age in number format: "))
    username = lastname[:3] + name

    while check_duplicate_user(username):
        username = input("Duplicate user detected. Please enter new username")

    rights = query_user_rights()
    password = generate_password(name, lastname, age)
    # Dictionary of a user
    user =  {
        "name": " ".join([name, lastname]), 
        "age": age, 
        "username": username, 
        "rights": rights, 
        "password": password
        }
    return user

def main():
    global users_list # Allows us to access to global variable 'users_list'
    while True:
        print(f"{len(users_list)} Users in the system: ")
        for u in users_list:
            print(f"{u["username"]}: {u["rights"]}")
        user = ask_user_details()
        users_list.append(user)
        do_quit = input("Type 'quit' to exit or press enter to add another user: ")
        if do_quit == "quit":
            break


if __name__ == "__main__":
    main()
