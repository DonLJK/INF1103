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
+ Search_product (itemid: int)
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

    def search_prod(self, id):
        for items in self.__inventory:
            if items.get_product_id() == id:
                return items
        print("product not found")
        return 
            

    def store_product(self, product): #Storing existing values
        self.__inventory.append(product)

    def add_product(self, product): #Storing new values into current inventory filled
        self.__inventory.append(product)

    def display_all(self):
        for item in self.__inventory:
            item.display_information()


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

    def get_user_input():
        user_choice = input("\nSelect an Option: ")
        return int(user_choice)
    
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


Menu.show()
my_inventory = load_inventory()
while True:
    choice = Menu.get_user_input()
    if choice == 1:
        my_inventory.display_all()
    elif choice == 2: 
        print("==== ADD PRODUCT ====")
        productid = input("Product id: ")
        prod_name = input("Product name: ")
        prod_price = input("Product price: ")
        prod_qty = input("Product Stock: ")

        my_inventory.add_product(productid, prod_name, prod_price, prod_qty)
    elif choice == 3:
        print("=====Update Product====")
        pid = int(input("Product"))
        item = my_inventory.search_prod(pid)
        if item is not None:
            print("item found: ", )
            qty = input("New Stock value: ")
            item.update_stock(qty)
            print("Stock updated!")
        else:
            print("Product not found.")

    elif choice == 6:
        break

        
