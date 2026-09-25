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
    prop_total = total + int(new_value)
    if prop_total > 500:
        print("\nDelivery skipped: inventory limit would be exceeded.")
        print("Current Inventory total: ", total)
        return total, False
    return prop_total, True
    

def calculate_tax(amnt):
    tax = amnt * 10/100
    #This function takes a delivery amount 
    #and returns the tax (10% of that specific delivery)
    return tax


def generate_report(total_u, failed_attempts, tax_revenue, stonks):
    #A dedicated function to print the final summary
    print("\nTotal units: ", total_u, "\nFailed attempts: ", failed_attempts, "\nTax for delivery: $", tax_revenue)
    #with open("inventory.txt", "w") as file:
    with open("inventory.txt", "w") as file:
        for each in stonks:
            file.write(str(each[0]) + ", " + each[1] + ", " + str(each[2]) + "\n")
        print("\nOrder Successfully saved to Inventory.txt")

        file.write(
            "==================\nFINAL REPORT\n"
            f"Total units: {total_u}\n"
            f"Failed attempts: {failed_attempts}\n"
            f"Tax for delivery: ${tax_revenue}\n"
        )
    # ^ Code above here recommended by AI, Makes all of the code below herev into text and simpler for me to run so that i dont have to insert values
    # file.write("\nTotal units: ", total_u, "\nFailed attempts: ", failed_attempts, "\nTax for delivery: $", tax_revenue)
    #    file.write("Total units: ", total_u, "\n", "Failed Attempts: ", )
    return

def load_inventory():
    stonks = []
    inventory = 0
     #open and read file, if file does not exist, create new file
    try: #tries to run this code
        opened_file = open("inventory.txt", "r")
        with open("inventory.txt", "r") as file:
            for items in file: #iterates within each item inside file
                #values read from file
                #input each line into file
                items = items.strip()#takes out each line from file and input into items
                if items == "==================":#Checks each line with this value to cut off when reach Final report
                    break

                fields = items.split(", ") #Splits the sentence on that particular ',' value
                if len(fields) == 3:
                    order_id, name, qty = fields
                    order_id = int(order_id)
                else:
                    name, qty = fields
                    order_id = 1001 + len(stonks)
                quant = int(qty)
                inventory, accepted = process_delivery(inventory, quant)
                if accepted:
                    stonks.append([order_id, name, qty])
                
        return inventory, stonks
    except FileNotFoundError: #Catches any errors and print
        print("Existing File does not exist, generating new copy")
        open("inventory.txt", "x").close()
    else:
         print("File is currently empty")
    return

def save_inventory(item, num, stonks):
    next_id = max((order[0] for order in stonks), default=0) + 1
    stonks.append([next_id, item, num])
    print("\nnew order added:\n", next_id, ",", item, ",", num)
    print("Order successfully added to inventory.txt")
    #stonkers = str(stonks)
    #create UID for each item saved
    return stonks


#variables
error_count = 0
num = 0
price = 0
inventory, stonks = load_inventory()

while True:     
        #This code prints
        print("\ncurrent orders:\n")
        for i in stonks:
            print(i[0], i[1], i[2]) 
        item_name = input ("\nEnter Item name: ")
        if item_name == "quit":
            break
        num = get_valid_input()
        if num == "terminate":
             break
        elif num == "error":
             error_count += 1
             continue
        else:
            inventory, accepted = process_delivery(inventory, num)
            if accepted:
                stonks = save_inventory(item_name, num, stonks)

price = calculate_tax(inventory)
generate_report(inventory, error_count, price, stonks)
print("========================")
print("Session Terminated")

        

