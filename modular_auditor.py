
def get_valid_input():
    #Handles the prompt, handles input validation, and
    #returns a valid integer or a "quit" signal.
    val = input("Enter stock quantity: ")
    if val == "quit":
        return "terminate"
    elif val.isdigit() != True: 
        print("Invalid Value, please try again")
        return "error"

    else:
        return int(val)
    
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
    return


#variables
inventory = 0
count = 0
num = 0
price = 0
while True:
        num = get_valid_input()
        if num == "terminate":
             break
        elif num == "error":
             count += 1
        else:
            inventory = process_delivery(inventory, num)
price = calculate_tax(inventory)
generate_report(inventory, count, price)
print("========================")
print("Session Terminated")

        

