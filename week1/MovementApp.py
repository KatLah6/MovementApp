# Week 1 - Movement App

Name= input("What is your first name?")
Lastname= input("What is your last name?")
Birthday= input("Write your birthday in the format dd/mm/yyyy: ")

print(f"Hello {Name} {Lastname}, welcome to the Motion Detector! Let's start. ")
username= Name[:2] + Lastname[:3] + Birthday[6:]+Birthday[3:5]+Birthday[0:2]


print(f"Your username is: {username} ")

Movement= input("Has there been movement in the room (Yes/No)?: ")
print(f"Movement detected: {Movement}")

#Convert C to F
def celsius_to_fahrenheit(celsius):
    fahrenheit= (celsius * 9/5) + 32
    return int(fahrenheit)

Temperature=input("What is the temperature of the room in °C?: ")

#Conversion
Temperature_f= celsius_to_fahrenheit(float(Temperature))

print(f"The given temperature {Temperature}°C is {Temperature_f}°F ")





# Week 2 - Movement App

