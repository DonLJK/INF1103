import math
import json
from abc import ABC, abstractmethod

class Supplier:
    def __init__(self, Supplier_id, name, email):
        self.supplier_id = Supplier_id
        self.supplier_name = name
        self.supplier_email = email
        return

    def display_information(self):
        return print(f"Supplier ID: {self.supplier_id}\nSupplier Name: {self.supplier_name}\nSupplier Email: {self.supplier_email}")


class Product(ABC):
    def __init__ (self, productid:int, name:str, price:float, stock:int, supplier: Supplier):
        self.__productid = productid
        self.__productname = name
        self.__productprice = price
        self.__productstock = stock

        self.supplier: Supplier = supplier

    def update_stock(self, quantity):
        self.__productstock = quantity

    def display_information(self):
        print(f"ID: {self.__productid} | Name: {self.__productname} | Price:  {self.__productprice} | Stock: {self.__productstock}")
        return 

    def get_product_id(self):
        return self.__productid

    def get_product_name(self):
        return self.__productname

    def get_product_price(self):
        return self.__productprice

    def get_product_stock(self):
        return self.__productstock

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def display_supply_info(self):
        self.supplier.display_information()

    def get_supply_info(self):
        return self.supplier.supplier_id, self.supplier.supplier_name, self.supplier.supplier_email

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Physicalproduct(Product, CanBeShipped):
    def __init__ (self, productid, name, price, stock, supplier, weight):
        self.__productweight = weight
        super().__init__(productid, name, price, stock, supplier)

    def display_information(self):
        print(f"ID: {self.get_product_id()} | Name: {self.get_product_name()} | Price:  {self.get_product_price()} | Stock: {self.get_product_stock()} | Weight: {self.__productweight}")

    def get_fulfilment_info(self):
        return "Product requires physical shipping"

    def calculate_shipping_cost(self):
        s_cost = self.__productweight * 0.10
        return s_cost

    def get_weight(self):
        return self.__productweight

    def update_weight(self, weight):
        self.__productweight = weight

    def display_supply_info(self):
        self.supplier.display_information()

class DigitalProduct(Product):
    def __init__ (self, productid, name, price, stock, supplier, dwn_size):
        self.__dwn_size = dwn_size
        super().__init__(productid, name, price, stock, supplier)

    def display_information(self):
        print(f"ID: {self.get_product_id()} | Name: {self.get_product_name()} | Price:  {self.get_product_price()} | Stock: {self.get_product_stock()} | Download Size: {self.__dwn_size}")

    def get_fulfilment_info(self):
        return "Product is delivered digitally"

    def get_download_size(self):
        return self.__dwn_size

    def display_supply_info(self):
        self.supplier.display_information()

class Inventory:
    def __init__(self):
        self.__inventory: list[Product] = []

    def get_product(self, id: str) -> Product|None:
        for items in self.__inventory:
            if items.get_product_id() == id:
                print("\n-----PRODUCT FOUND!-----") 
                print("Item ID: ",items.get_product_id())
                print("Item name: ",items.get_product_name())
                print("Item Price: ", items.get_product_price())
                print("Stock: ", items.get_product_stock())
                return items
        print("product not found")
        return 

    def get_next_id(self):
        return max((product.get_product_id() for product in self.__inventory), default=100,) + 1

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

    def add_product(self, product: Product) -> None: 
        self.__inventory.append(product)
        print("Product Added!")

    def display_all(self):
        if not self.__inventory:
            return print("Empty Inventory")
        for item in self.__inventory:
            item.display_information()

    def calculate_tax(self):
        stock = self.get_total_stocks()
        tax = int(stock) * 10/100
        return tax

    def remove(self,item_id: str) ->None:
        for product in self.__inventory:
            if str(product.get_product_id()) == item_id: #I used get&set methods from C++ days
                self.__inventory.remove(product) #remove was a thing for python lists that i forgot
                print("Product Removed")
                return

        


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
        try:
            user_choice = int(input("\nSelect an Option: "))
        except ValueError:
            print("Invalid Value")
        return user_choice

    def display_options():
        print("1. Physical product")
        print("2. Digital product")

def get_valid_input():
        qty = input("Enter stock quantity: ")
        if qty == "quit":
            return None
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
        product_type = i.get("type")
        supplier_data = i["supplier"]
        supplier = Supplier(
            supplier_data["supplier_id"],
            supplier_data["supplier_name"],
            supplier_data["supplier_email"]
        )
        if product_type == "physical":

            item = Physicalproduct(
                i["order_id"],
                i["item_name"],
                i["item_price"],
                i["qty"],
                supplier,
                i["weight"]
            )

        elif product_type == "digital":

            item = DigitalProduct(
                i["order_id"],
                i["item_name"],
                i["item_price"],
                i["qty"],
                supplier,
                i["download_size"]
            )
        else:
            print(f"Skipping product with missing or unknown type: {i.get('order_id', 'unknown ID')}")
            continue

        inventory.store_product(item)
    return inventory

def generate_and_save_report(inventory, failed, tax):
    inv = []
    total_ship = 0
    for product in inventory.get_inventory():
        product_data = {
            "order_id": product.get_product_id(),
            "item_name": product.get_product_name(),
            "item_price": product.get_product_price(),
            "qty": product.get_product_stock(),
            "supplier": {
                "Supplier ID: ": product.supplier.supplier_id,
                "Supplier Name: ": product.supplier.supplier_name,
                "Supplier Email: ": product.supplier.supplier_email
            }
        }
        if isinstance(product, Physicalproduct):
            product_data["type"] = "physical"
            product_data["weight"] = product.get_weight()
            total_ship += product.calculate_shipping_cost()
        elif isinstance(product, DigitalProduct):
            product_data["type"] = "digital"
            product_data["download_size"] = product.get_download_size()
        else:
            raise TypeError(f"Unsupported product type: {type(product).__name__}")
        inv.append(product_data)

    data = {
        "stocks": inv,
        "report": {
            "total_units": inventory.get_total_stocks(),
            "failed_attempts": failed,
            "tax_revenue": tax,
            "Shipping cost": total_ship,
        },
    }

    with open("inventory.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved.")


# Create supplier
supplier = Supplier(1, "ABC Suppliers", "abc@gmail.com")

# Create product BEFORE inventory
keyboard = Physicalproduct(
    101, "Keyboard", 50.0, 10, supplier, 1.5
)

# Create two inventories
inventory_A = Inventory()
inventory_B = Inventory()

# Add product to A
inventory_A.add_product(keyboard)

# Remove product from A
inventory_A.remove("101")

# Check if product still exists
keyboard.display_information()

# Add SAME product to B
inventory_B.add_product(keyboard)

# Display B
inventory_B.display_all()
'''
supplier = Supplier(1, "ABC Suppliers", "abc@gmail.com")
error_count = 0
Menu.show() 
my_inventory = load_inventory()
while True:
    try:
        choice = Menu.get_user_input()
    except UnboundLocalError:
        print("Please Select 1-6")
        continue
    if choice == 1:
        print("\n====Displaying Inventory====\n")
        my_inventory.display_all()

    elif choice == 2: 
        print("==== ADD PRODUCT ====")
        Menu.display_options()
        u_choice = Menu.get_user_input()
        if u_choice <3 and u_choice>=1:
            n_id = my_inventory.get_next_id()
            print("Product ID: ", n_id)
            try:
                prod_name = input("Product name: ")
            except ValueError:
                print("Invalid ID")
                continue
            if prod_name == "quit":
                break

            result = get_valid_input()
            if result is None:
                break
            elif result == "error":
                    error_count += 1
                    continue
            price, num = result
            total = my_inventory.get_total_stocks()
            new_total = my_inventory.check_storage_space(total, num)

            if new_total == total and num > 0:
                continue

           
            if u_choice == 1:
                weight = float(input("Enter Product Weight(kg): "))
                new_item = Physicalproduct(n_id, prod_name, price, num, supplier, weight)
                
                new_item.display_supply_info()

            elif u_choice == 2:
                dwn_size = input("Enter Download size: ")
                new_item = DigitalProduct(n_id, prod_name, price, num, supplier, dwn_size)
                
                new_item.display_supply_info()
            
            my_inventory.add_product(new_item)
        else: 
            print("Out of bounds\nrestarting...")
            continue

    elif choice == 3:
        print("=====Update Product====")
        try:
            pid = int(input("Product ID: ")) 
        except ValueError:
            print("Invalid ID")
            continue
        item = my_inventory.get_product(pid)
        if item is not None:
            qty = input("New Stock value: ")
            total = my_inventory.get_total_stocks()
            new_total = my_inventory.check_storage_space(total, qty)
            if new_total == total:
                        continue
            item.update_stock(int(qty))
            print("Stock updated!")

    elif choice == 4:
        print("====Search Product====")
        pid = int(input("Product ID: "))
        my_inventory.get_product(pid)
            
    elif choice == 5:
        generate_and_save_report(my_inventory, error_count, my_inventory.calculate_tax())

    elif choice == 6:
        er_count = error_count
        tax =  my_inventory.calculate_tax()
        generate_and_save_report(my_inventory, error_count, my_inventory.calculate_tax())
        print("Saving inventory before exit...")
        print("Inventory Saved successfully\n\n")
        print("Program Terminated")
        break
    '''