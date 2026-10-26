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
        print("Product Stock:", self.__productstock)
        return 

class Inventory:
    def __init__(self):
        self.__inventory = []

    def store_product(self, product): #Storing existing values
        pass #Later implmentation with loading

    def add_product(self, product): #Storing new values into current inventory filled
        self.__inventory.append(product)

    def display_all(self):
        for item in self.__inventory:
            item.display_information()


"""
Menu:
-------------
+ display_menu()
+ get_user_input()
+ run(): void
"""

class Menu: #Cycle through options - for now also creates the products and inventory
    def show():
        print("========== Inventory Management =========")
        print("1. Display All Products")
        print("2. Add Products")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")

    def get_user_input():
        user_choice = input("\nSelect an Option: ")
        return int(user_choice)

my_inventory = Inventory()
mug = Product(101 , "pizza", 14.50, 10)
my_inventory.add_product(mug)
my_inventory.display_all()
Menu.show()
if Menu.get_user_input() == 1:
    my_inventory.display_all()


#my_inventory = Inventory()
#mug = Product(101 , "pizza", 14.50, 10)
#my_inventory.add_product(mug)
#my_inventory.display_all()

