#Smart Vending Machine
available_drinks = ["Coke", "Pepsi", "Water", "Juice"]

def check_drink(drink):
    
    if drink in available_drinks:
        return True
    else:
        print("Sorry Drink not available")
        return False


def dispense_drink(drink):
    print("Dispensing", drink, "... Enjoy!")


def funct(func,inp):
    #print("value was taken as", inp)
    return func(inp)
#i want it to take the value, put in
# then call another function to check if drink exists
# if yes dispense, else return


def dispenser_button(num):
    available_drinks = ["Coke", "Pepsi", "Water", "Juice"]
    #print("The value of num: ", num)
    match int(num): #I need to be aware this is taking a value as a string. so i need to convert it.
        case 1:
            return dispense_drink(available_drinks[0])
        case 2: 
            return dispense_drink(available_drinks[1])
        case 3:
            return dispense_drink(available_drinks[2])
        case 4:
            return dispense_drink(available_drinks[3])
        case _:
            return ("Value does not exist")
            

print("Hi please press a number for your drink\n1.Coke \n2.Pepsi \n3.Water, \n4.Juice")
number = input("Drink: ")#
funct(dispenser_button,number)
#print(dispenser_button(input("Drink: ")))