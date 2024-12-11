# user.py
# Define the User Class
class User:
    def __init__(self, username, email, name, password, birthdate):
        self.username = username
        self.email = email
        self.name = name
        self.password = password
        self.birthdate = birthdate

    def display_info(self):
        print(f"Username: {self.username}, Email: {self.email}")

    def to_dict(self):
        """
        Creates a dictionary containing User attributes
        :return: dict
        """
        return {
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "password": self.password,
            "birthdate": self.birthdate.strftime("%d/%m/%Y")
        }

# Implement User Roles

class Admin(User):
    def __init__(self, username, email, name, password, birthdate):
        super().__init__(username, email, name, password, birthdate)
        self.permissions = ["add_user", "remove_user", "view_all_users"]
    def display_permissions(self):
        print(f"Admin Permissions: {self.permissions}")

class SuperUser(Admin):
    def display_permissions(self):
        print(f"Super-User Permissions")

class RegularUser(User):
    def __init__(self, username, email, name, password, birthdate):
        super().__init__(username, email, name, password, birthdate)
        self.permissions = ["view_profile"]
    def display_permissions(self):
        print(f"User Permissions: {self.permissions}")