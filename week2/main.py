import random
from dateutil.relativedelta import *
from datetime import date
# Week 2 - Movement App
# Calculations assume tempature in Celsius. We'll do conversions on the output for the user

Teacher= "Mira"
Myself = "Katyuska"


def wrapped_input(query_str):
    result = input(query_str)
    if result == "quit":
        print("Thanks for visiting. Welcome back soon.")
        exit(0)
    return result

#Convert C to F
def celsius_to_fahrenheit(celsius):
    fahrenheit= (celsius * 9/5) + 32
    return int(fahrenheit)

def validate_brithday(input_str):
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

def calculate_age(birthday):
    day, month, year = birthday.split('/')
    today = date.today()
    dob = date(int(year), int(month), int(day))
    age = relativedelta(today, dob)
    return age.years

#Get user name
def ask_name_and_age():
    b_day_format = "dd/mm/yyyy"
    name = wrapped_input("What is your name? ")
    Birthday= wrapped_input(f"Write your birthday in the format {b_day_format}: ")
    while not validate_brithday(Birthday):
        Birthday = wrapped_input(f"Please enter a valid birthday in format {b_day_format}: ")
    age = calculate_age(Birthday)

    return name, age


#Check age
def check_age(age):
    if age < 18:
        return False
    else:
        return True

#Check user
def print_greeting(name):
    rights = "viewer"
    if name == Teacher:
        rights = "super-user"
    elif name == Myself:
        rights = "admin"
    welcome_msg = f"Welcome {name}, you have {rights} rights."
    print(welcome_msg)

def get_temp_string(tempature):
    if tempature > 100:
        return "ON_FIRE"
    if tempature > 90:
        return "TOO HOT"
    return "OK"

def get_sensor_data():
    tempature = random.randrange(40, 110)
    movement = random.randint(0, 1)
    return tempature, movement

def get_tempature_format():
    tempature_format=wrapped_input("Do you want the temperature in °C or °F? [C, F]: ")
    while not tempature_format in ["C", "F"]:
        tempature_format = wrapped_input("Please enter the temperature format in either °C or °F [C, F]: ")
    return tempature_format

def main():
    # https://www.w3schools.com/python/python_tuples_unpack.asp
    (name, age) = ask_name_and_age()
    if not check_age(age):
        print(f"Grettings {name} you are too young to operate this program. ")
        print("Thanks for visiting.")
        exit(1)
    temp_format = get_tempature_format()
    print_greeting(name)
    (tempature, movement) = get_sensor_data()
    temp_str = get_temp_string(tempature)
    if temp_format == "F":
        tempature = celsius_to_fahrenheit(tempature)
    print(f"The temperature of the CPU is {tempature} °{temp_format}, it is {temp_str}")
    # Ternary operator for short code https://www.geeksforgeeks.org/ternary-operator-in-python/
    print(f"{"Movement detected" if movement else "Movement not detected"}") 
    user_input = ""
    while user_input != "quit":
        user_input = input("Type 'quit' to exit: ")

if __name__ == "__main__":
    main()
