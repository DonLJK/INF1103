import math
import json
#UML
'''
#Product class should not be responsible for
loading
saving
displaying
asking user for input
managing entire inventory

PRODUCT: 
- __productid
- __name
- __price
- __stock
-----------------
+ update_stock(quantity:int)void
+ display_information():void

Inventory:
-------------
+ store_product(product:List)
+ add_product(itemname: String)
+ get_productuct (itemid: int)
+ display_all():void

Menu:
-------------
+ display_menu()
+ get_user_input()
+ run(): void

FileHandler:
-------------
+ Load_inventory(): List<Product>
+ Save_inventory(product:List)

Objects: Inventory_System, Products, menu, file

'''
class Product:
    def __init__ (self, productid, name, price, stock):
        self.__productid = productid
        self.__productname = name
        self.__productprice = price
        self.__productstock = stock

    def update_stock(self, quantity):
        self.__productstock = quantity

    def display_information(self):
        print("Product ID:", self.__productid)
        print("Product Name:", self.__productname)
        print("Product Price:",  self.__productprice)
        print("Product Stock:", self.__productstock, "\n")
        return 

    def get_product_id(self):
        return self.__productid

    def get_product_name(self):
        return self.__productname

    def get_product_price(self):
        return self.__productprice

    def get_product_stock(self):
        return self.__productstock

class Inventory:
    def __init__(self):
        self.__inventory = []

    def get_product(self, id):
        for items in self.__inventory:
            if items.get_product_id() == id:
                print("\n-----PRODUCT FOUND!-----") 
                print("Item ID: ",items.get_product_id())
                print("Item name: ",items.get_product_name())
                print("Item Price: ", items.get_product_price())
                print("Stock: ", items.get_product_stock())
                return items
            else:
                print("product not found")
        return 

    def get_next_id(self):
        return max(
            (product.get_product_id() for product in self.__inventory),
            default=100,
        ) + 1

    def get_inventory(self):
        return self.__inventory.copy()

    def get_total_stocks(self):
        total = sum(items.get_product_stock() for items in self.__inventory)
        return total

    def check_storage_space(self, total_stocks, qty):
        new_total = total_stocks + int(qty)
        if new_total > 500:
            print("\nDelivery skipped: inventory limit would be exceeded.")
            print("Current Inventory total: ", total_stocks)
            return total_stocks
        return new_total

    def store_product(self, product): #Storing existing values
        self.__inventory.append(product)

    def add_product(self, product): #Storing new values into current inventory filled
        self.__inventory.append(product)
        print("Product Saved!")

    def display_all(self):
        for item in self.__inventory:
            item.display_information()

    def calculate_tax(self):
        tax = self.get_total_stocks() * 10/100
        return tax


class Menu: #Cycle through options - for now also creates the products and inventory
    def show():
        print("==========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("==========================================\n")
        print("1. Display All Products")
        print("2. Add Products")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

    def get_user_input():
        user_choice = input("\nSelect an Option: ")
        return int(user_choice)

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
        
    
def load_inventory():
    try:
        inventory = Inventory()
        with open("inventory.json", "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                print("inventory.json is empty, starting with new inventory")
                return inventory
            data = json.loads(content)
    except FileNotFoundError:
        print("inventory.json not found, starting with empty inventory")
        return inventory
    except json.JSONDecodeError:
        print("inventory.json is corrupted or invalid, starting with empty inventory")
        return inventory

    loaded_stocks = data.get("stocks", [])
    for i in loaded_stocks:
        item = Product(i["order_id"],i["item_name"], i["item_price"], i["qty"])
        inventory.store_product(item)
    return inventory



def generate_and_save_report(inventory, failed, tax):
    inv = [
        {
            "order_id": product.get_product_id(),
            "item_name": product.get_product_name(),
            "item_price": product.get_product_price(),
            "qty": product.get_product_stock(),
        }
        for product in inventory.get_inventory()
    ]

    data = {
        "stocks": inv,
        "report": {
            "total_units": inventory.get_total_stocks(),
            "failed_attempts": failed,
            "tax_revenue": tax,
        },
    }

    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved.")

error_count = 0
Menu.show() 
my_inventory = load_inventory()
while True:
    choice = Menu.get_user_input()
    if choice == 1:
        print("\n====Displaying Inventory====\n")
        my_inventory.display_all()

    elif choice == 2: 
        print("==== ADD PRODUCT ====")
        n_id = my_inventory.get_next_id()
        print("Product ID: ", n_id)
        prod_name = input("Product name: ")
        if prod_name == "quit":
            break
        result = get_valid_input()
        if result == "terminate":
                break
        if result == "error":
                error_count += 1
                continue
        price, num = result
        total = my_inventory.get_total_stocks()
        new_total = my_inventory.check_storage_space(total, num)
        if new_total == total and num > 0:
            continue
        new_item = Product(n_id, prod_name, price, num)
        my_inventory.add_product(new_item)

    elif choice == 3:
        print("=====Update Product====")
        pid = int(input("Product ID: "))
        item = my_inventory.get_product(pid)
        if item is not None:
            qty = input("New Stock value: ")
            item.update_stock(qty)
            print("Stock updated!")
        else:
            print("Product not found.")

    elif choice == 4:
        print("====Search Product====")
        pid = int(input("Product ID: "))
        my_inventory.get_product(pid)
            
    elif choice == 5:
        er_count = error_count
        generate_and_save_report(my_inventory, er_count, my_inventory.calculate_tax())

    elif choice == 6:
        break
