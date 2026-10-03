
#====== Lab 5 ======#
#Defining new functions
#cart = {
#
#}

import json
import math


stocks = []



def add_product(order_id, item_name, item_price, qty):
    stocks.append({
                    "order_id": order_id,
                    "item_name": item_name,
                    "item_price": item_price,
                    "qty": qty
                    })
    #print(stocks)
    return

def update_stock(id):
    prodid = input("Enter Product ID: ")
    if not prodid.isdigit():
        print("Invalid ID, please enter a number")
        return
    
    target_id = int(prodid)
    for i in range(len(stocks)):
        if stocks[i]["order_id"] == target_id:
            print("Current item:", stocks[i]["item_name"], "| Qty:", stocks[i]["qty"])
            new_qty = input("New Quantity: ")
            if new_qty.isdigit():
                stocks[i]["qty"] = int(new_qty)
                print("Quantity updated to", new_qty)
            else:
                print("Invalid quantity, update cancelled")
            return
    
    print("No product found with that ID")

def search_product(productid):
    try:
        p_id = int(productid)
    except ValueError:
        print("Invalid Product ID, please enter a number")
        return

    # Search by order_id instead of list index
    found = False
    for product in stocks:
        if product["order_id"] == p_id:
            print("--------------")
            print("ID:", product["order_id"])
            print("Name:", product["item_name"])
            print("Price:", product["item_price"])
            print("Stock:", product["qty"])
            print("--------------")
            found = True
            break

    if not found:
        print("Product with ID", p_id, "not found")

def display_all():
    print(stocks)

#============#

def get_valid_input():
    qty = input("Enter stock quantity: ")
    if qty == "quit":
        return "terminate"
    if not qty.isdigit():
        print("Invalid Value, please try again")
        return "error"

    item_price = input("Price: ")
    try:
        price = float(item_price)
    except ValueError:
        print("Invalid price, please try again")
        return "error"

    if not math.isfinite(price) or price < 0:
        print("Price must be a finite, non-negative number")
        return "error"

    return price, int(qty)
    
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


def generate_report(total_u, failed_attempts, tax_revenue, stocks):
    #print(
    #    "Total units:", total_u,
    #    "\nFailed attempts:", failed_attempts,
    #    "\nTax for delivery: $", tax_revenue,
    #)
    print("\nInventory items:")
    for product in stocks:
        print("p",product["order_id"], ".", product["item_name"], "| Price: $", product["item_price"], "| Qty:", product["qty"])

    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(
            {
                "stocks": stocks,
                "report": {
                    "total_units": total_u,
                    "failed_attempts": failed_attempts,
                    "tax_revenue": tax_revenue,
                },
            },
            file,
            indent=4,
        )
    print("\nOrders and report saved to inventory.json")
    return

def load_inventory():
    try:
        with open("inventory.json", "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                print("inventory.json is empty, starting with new inventory")
                return 0, []
            data = json.loads(content)
    except FileNotFoundError:
        print("inventory.json not found, starting with empty inventory")
        return 0, []
    except json.JSONDecodeError:
        print("inventory.json is corrupted or invalid, starting with empty inventory")
        return 0, []

    loaded_stocks = data.get("stocks", [])
    inventory = sum(int(product["qty"]) for product in loaded_stocks)
    print("inventory.json loaded successfully")
    return inventory, loaded_stocks

def save_inventory(next_id, item, price, num, stonks):
    add_product(next_id, item, price, num)
    print("\nnew order added:\n", "ID:", next_id, ", " ,"Item name:", item, ", " ,"Item price:", price, ", " ,"Item num:", num)
    print("Order successfully added")
    return stonks



#variables
error_count = 0
num = 0
price = 0


print("==========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("==========================================\n")

inventory, stocks = load_inventory()

print("\n======MENU======")
print("1. Display All products\n2. Add Product\n3. Update stock\n4. Search Product\n5. Save Inventory\n6. Exit")
print("=================")
    
while True: 
        #This code prints
    choice = input("\nEnter Option: ")
    match choice:
        case "1":
            print("\ncurrent orders:\n")
            for i in stocks:
                print("ID:", i["order_id"], "|Name:", i["item_name"], "|price:", i["item_price"], "|Stock:", i["qty"])

        case "2":
            print("Add new product")
            next_id = max((order["order_id"] for order in stocks), default=100) + 1
            print("Product ID: ", next_id)
            item_name = input("Enter Item name: ")
            if item_name == "quit":
                break
            result = get_valid_input()
            if result == "terminate":
                break
            if result == "error":
                error_count += 1
                continue
            price, num = result
            inventory, accepted = process_delivery(inventory, num)
            if accepted:
                stocks = save_inventory(next_id, item_name, price, num, stocks) #Saves into dictionary

        case "3":  # update
            print("===UPDATE STOCK===")
            update_stock(stocks)
        case "4":  # Search
            print("===PRODUCT SEARCH===")
            if len(stocks) == 0:
                            print("Dictionary is empty")
            else:
                productid = input("Enter Product ID: ")
                search_product(productid)
        case "5":
            print("Saving inventory")
            tax_revenue = calculate_tax(inventory)
            generate_report(inventory, error_count, tax_revenue, stocks)
        case "6":
            print("Saving...")
            tax_revenue = calculate_tax(inventory)
            generate_report(inventory, error_count, tax_revenue, stocks)
            print("Inventory Saved")
            print("Thank you for using Inventory Management System \nSession Terminated")
            break
        case _:
            print("Invalid Option, Please select from 1 to 6")
            

        
                




        

