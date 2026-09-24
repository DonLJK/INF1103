def get_valid_input():
    #Handles the prompt, handles input validation, and
    #returns a valid integer or a "quit" signal.

    item_name = input("Enter item name :")
    val = input("Enter stock quantity: ")
    if val == "quit":
        return "terminate"
    elif val.isdigit() != True: 
        print("Invalid Value, please try again")
        return "error"
    else:
        return item_name, int(val)
    
def process_delivery(total, new_value):
    total = total + new_value
    print("Current total: ", total)
    #Calculates the new total and returns it
    return total

def calculate_tax(amnt):
    tax = amnt * 10/100
    #This function takes a delivery amount 
    #and returns the tax (10% of that specific delivery)
    return tax


def generate_report(total_u, failed_attempts, tax_revenue):
    #A dedicated function to print the final summary
    print("\nTotal units: ", total_u, "\nFailed attempts: ", failed_attempts, "\nTax for delivery: $", tax_revenue)
    #with open("inventory.txt", "w") as file: 
    #    file.write("Total units: ", total_u, "\n", "Failed Attempts: ", )
    return

def load_inventory():
    #open and read file, if file does not exist, create new file
    print("current orders:")
    try: #tries to run this code
        opened_file = open("inventory.txt", "r")
        print(opened_file.readlines())
    except FileNotFoundError: #Catches any errors and print
        print("Existing File does not exist, generating new copy")
        open("inventory.txt", "x").close()

    return

def save_inventory(item, num, stonks):
    stonks.append(item)
    stonks.append(num)
    with open("inventory.txt", "w") as file:
                    for i in stonks:  
                        file.write(i)
                    file.close()
    return


#variables
inventory = 0
count = 0
num = 0
price = 0
stonks = []
while True:
        load_inventory()
        item, num = get_valid_input()
        if num == "terminate":
             break
        elif num == "error":
             count += 1
        else:
            inventory = process_delivery(inventory, num)
            if inventory > 500:
                print("Currently over limit by: ", inventory - 500)
                break
            else:
                save_inventory(item,num,stonks)
                #print(stonks) #prints out list
                
            
            
price = calculate_tax(inventory)
generate_report(inventory, count, price)
print("========================")
print("Session Terminated")

        

