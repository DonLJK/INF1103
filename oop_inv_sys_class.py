import _io
import io
import math
import json
import abc
import typing

class Supplier:
    def __init__(self, Supplier_id: int, name: str, email: str) -> None:
        self.supplier_id:int = Supplier_id
        self.supplier_name:str = name
        self.supplier_email:str = email
        return

    def display_information(self) -> None:
        return print(f"Supplier ID: {self.supplier_id}\nSupplier Name: {self.supplier_name}\nSupplier Email: {self.supplier_email}")


class Product(abc.ABC):#Used Source-Action apply all annotation to save time for subsequent singatures
    def __init__ (self, productid:int, name:str, price:float, stock:int, supplier: Supplier) -> None:
        self.__productid: int = productid
        self.__productname: str = name
        self.__productprice: float = price
        self.__productstock: int = stock

        self.supplier: Supplier = supplier

    def update_stock(self, quantity:int) -> None:
        self.__productstock: int = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__productid} | Name: {self.__productname} | Price:  {self.__productprice} | Stock: {self.__productstock}")
        return 

    def find_product_id(self) -> int:
        return self.__productid

    def find_product_name(self) -> str:
        return self.__productname

    def find_product_price(self) -> float:
        return self.__productprice

    def find_product_stock(self) -> int:
        return self.__productstock

    @abc.abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def display_supply_info(self) -> None:
        self.supplier.display_information()

    def get_supply_info(self) -> tuple[int, str, str]:
        return self.supplier.supplier_id, self.supplier.supplier_name, self.supplier.supplier_email

class CanBeShipped(abc.ABC):
    @abc.abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass

class Physicalproduct(Product, CanBeShipped):
    def __init__ (self, productid:int, name:str, price:float, stock:int, supplier:Supplier, weight:float) -> None:
        self.__productweight: typing.Any = weight
        super().__init__(productid, name, price, stock, supplier)

    def display_information(self) -> None:
        print(f"ID: {self.find_product_id()} | Name: {self.find_product_name()} | Price:  {self.find_product_price()} | Stock: {self.find_product_stock()} | Weight: {self.__productweight}")

    def get_fulfilment_info(self) -> str:
        return "Product requires physical shipping"

    def calculate_shipping_cost(self) -> float:
        s_cost = self.__productweight * 0.10
        return s_cost

    def get_weight(self) -> float:
        return self.__productweight

    def update_weight(self, weight:float) -> None:
        self.__productweight = weight

    def display_supply_info(self) -> None:
        self.supplier.display_information()

class DigitalProduct(Product):
    def __init__ (self, productid:int, name:str, price:float, stock:int, supplier:Supplier, dwn_size:str) -> None:
        self.__dwn_size: typing.Any = dwn_size
        super().__init__(productid, name, price, stock, supplier)

    def display_information(self) -> None:
        print(f"ID: {self.find_product_id()} | Name: {self.find_product_name()} | Price:  {self.find_product_price()} | Stock: {self.find_product_stock()} | Download Size: {self.__dwn_size}")

    def get_fulfilment_info(self) -> str:
        return "Product is delivered digitally"

    def get_download_size(self) -> str:
        return self.__dwn_size

    def display_supply_info(self) -> None:
        self.supplier.display_information()

class Inventory:
    def __init__(self) -> None:
        self.__inventory: list[Product] = []

    def find_product(self, id: str) -> Product|None:
        for items in self.__inventory:
            if items.find_product_id() == id:
                return items
        return None 

    def get_next_id(self) -> int:
        return max((product.find_product_id() for product in self.__inventory), default=100,) + 1

    def get_inventory(self) -> list[Product]:
        return self.__inventory.copy()

    def get_total_stocks(self) -> int:
        total: int = sum(items.find_product_stock() for items in self.__inventory)
        return total

    def check_storage_space(self, total_stocks:int , qty:int) -> int:
        new_total = total_stocks + int(qty)
        if new_total > 500:
            print("\nDelivery skipped: inventory limit would be exceeded.")
            print("Current Inventory total: ", total_stocks)
            return total_stocks
        return new_total

    def store_product(self, product) -> None: #Storing existing values
        self.__inventory.append(product)

    def add_product(self, product: Product) -> None: 
        self.__inventory.append(product)
        print("Product Added!")

    def display_all(self) -> None:
        if not self.__inventory:
            return print("Empty Inventory")
        for item in self.__inventory:
            item.display_information()
            #print(item.get_fulfilment_info())

    def calculate_tax(self) -> float:
        stock: int = self.get_total_stocks()
        tax: float = int(stock) * 10/100
        return tax

    def remove(self,item_id: str) ->None:
        for product in self.__inventory:
            if str(product.find_product_id()) == item_id: #I used get&set methods from C++ days
                self.__inventory.remove(product) #remove was a thing for python lists that i forgot
                print("Product Removed")
                return


class OrderLine: 
    def __init__(self, product:Product, qty: int) -> None:
        self.product: Product = product
        self.quantity: int = qty

    def calculate_subtotal(self) -> float:
        return self.product.find_product_price() * self.quantity


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            print("Quantity must be greater than zero.")
            return

        if quantity > product.find_product_stock():
            print("Insufficient stock!")
            return

        order_line: OrderLine = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total_value: float = 0.0

        for order_line in self.order_lines:
            total_value += order_line.calculate_subtotal()

        return total_value

    def display_order(self) -> None:
        print(f"\n===== ORDER {self.order_id} =====")

        for order_line in self.order_lines:
            print(
                f"{order_line.product.find_product_name()} | "
                f"Quantity: {order_line.quantity} | "
                f"Subtotal: ${order_line.calculate_subtotal()}"
            )

        print(f"Total: ${self.calculate_total()}")

class OrderManager:

    def __init__(self, inventory: Inventory) -> None:
        self.inventory: Inventory = inventory
        self.orders: list[Order] = []

    def create_order(self) -> None:
        order = Order(f"ORD{len(self.orders) + 1}")

        while True:
            self.inventory.display_all()

            try:
                pid: int = int(input("Enter Product ID: "))
                qty: int = int(input("Enter Quantity: "))
            except ValueError:
                print("Invalid input!")
                continue

            product: Product | None = self.inventory.find_product(pid)

            if product is None:
                continue

            order.add_order_line(product, qty)

            another: str = input(
                "Add another product? (y/n): "
            ).lower()

            if another != "y":
                break

        order.display_order()
        self.orders.append(order)

class Menu: #Cycle through options - for now also creates the products and inventory
    def show() -> None:
        print("==========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("==========================================\n")
        print("1. Display All Products")
        print("2. Add Products")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. remove item")
        print("7. create customer order")
        print("8. Exit")

    def get_user_input() -> int:
        try:
            user_choice = int(input("\nSelect an Option: "))
        except ValueError:
            print("Invalid Value")
        return user_choice

    def display_options() -> None:
        print("1. Physical product")
        print("2. Digital product")

def get_valid_input() -> None | tuple[float, int] | str:
        qty: str = input("Enter stock quantity: ")
        if qty == "quit":
            return None
        if not qty.isdigit():
            print("Invalid Value, please try again")
            return "error"
        item_price: str = input("Price: ")
        try:
            price = float(item_price)
        except ValueError:
            print("Invalid price, please try again")
            return "error"

        if not math.isfinite(price) or price < 0:
            print("Price must be a finite, non-negative number")
            return "error"

        return price, int(qty)
        
    
def load_inventory() -> Inventory:
    try:
        inventory = Inventory()
        with open("inventory.json", "r", encoding="utf-8") as file: 
            content: str = file.read().strip()
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

            item: Physicalproduct[typing.Any, typing.Any, typing.Any, typing.Any, Supplier, typing.Any] = Physicalproduct(
                i["order_id"],
                i["item_name"],
                i["item_price"],
                i["qty"],
                supplier,
                i["weight"]
            )

        elif product_type == "digital":

            item: DigitalProduct[typing.Any, typing.Any, typing.Any, typing.Any, Supplier, typing.Any] = DigitalProduct(
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

def generate_and_save_report(inventory, failed, tax, orders:list[Order]) -> None:
    inv = []
    order_data = []
    total_ship = 0
    for order in orders:
        order_data.append({
            "order_id": order.order_id,
            "items": [
                {
                    "product_id": line.product.find_product_id(),
                    "item_name": line.product.find_product_name(),
                    "quantity": line.quantity,
                    "subtotal": line.calculate_subtotal(),
                }
                for line in order.order_lines
            ],
            "total": order.calculate_total(),
        })

    for product in inventory.get_inventory():
        product_data = {
            "order_id": product.find_product_id(),
            "item_name": product.find_product_name(),
            "item_price": product.find_product_price(),
            "qty": product.find_product_stock(),
            "supplier": {
                "supplier_id": product.supplier.supplier_id,
                "supplier_name": product.supplier.supplier_name,
                "supplier_email": product.supplier.supplier_email
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
        "orders": order_data,
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

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


supplier = Supplier(1, "ABC Suppliers", "abc@gmail.com")
error_count = 0
Menu.show() 
my_inventory = load_inventory()
customer_order = OrderManager(my_inventory)
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
            n_id: int = my_inventory.get_next_id()
            print("Product ID: ", n_id)
            try:
                prod_name: str = input("Product name: ")
            except ValueError:
                print("Invalid ID")
                continue
            if prod_name == "quit":
                break

            result: None | tuple[float, int] | str = get_valid_input()
            if result is None:
                break
            elif result == "error":
                    error_count += 1
                    continue
            price, num = result
            total: int = my_inventory.get_total_stocks()
            new_total: int = my_inventory.check_storage_space(total, num)

            if new_total == total and num > 0:
                continue

           
            if u_choice == 1:
                weight = float(input("Enter Product Weight(kg): "))
                new_item= Physicalproduct(n_id, prod_name, price, num, supplier, weight)
                del supplier
                new_item.display_supply_info()

            elif u_choice == 2:
                dwn_size: str = input("Enter Download size: ")
                new_item = DigitalProduct(n_id, prod_name, price, num, supplier, dwn_size)
                del supplier    
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
        item: Product | None = my_inventory.find_product(pid)
        if item is None:
            print("Product Not found")
        elif item is not None:
            print("==Product Found!==")
            qty: str = input("New Stock value: ")
            total: int = my_inventory.get_total_stocks()
            new_total: int = my_inventory.check_storage_space(total, qty)
            if new_total == total:
                        continue
            item.update_stock(int(qty))
            print("Stock updated!")

    elif choice == 4:
        print("====Search Product====")
        pid = int(input("Product ID: "))
        item = my_inventory.find_product(pid)
        if item is None: 
            print("Product Not Found")
        elif item is not None:
            print("==Product Found!==")
            item.display_information()
            
    elif choice == 5:
        generate_and_save_report(my_inventory, error_count, my_inventory.calculate_tax(), customer_order.orders)

    elif choice == 6:
        pid = int(input("Product ID: "))
        my_inventory.remove(pid)

    elif choice == 7: #Creates customer order 
        customer_order.create_order()

    elif choice == 8:
        er_count: int = error_count
        tax: float =  my_inventory.calculate_tax()
        generate_and_save_report(my_inventory, error_count, my_inventory.calculate_tax(), customer_order.orders)
        print("Saving inventory before exit...")
        print("Inventory Saved successfully\n\n")
        print("Program Terminated")
        break


''' #Test generated by AI
def test_oop() -> None:

    supplier = Supplier(1, "ABC Suppliers", "abc@gmail.com")

    # Create both product types
    physical = Physicalproduct(101, "Laptop", 1200, 10, supplier, 2.5)
    digital = DigitalProduct(102, "E-Book", 20, 50, supplier, "15MB")

    # POLYMORPHISM: Store both as Product references
    inventory = Inventory()
    product1: Product = physical
    product2: Product = digital

    inventory.add_product(product1)
    inventory.add_product(product2)

    print("\n===== POLYMORPHISM TEST =====")

    for product in inventory.get_inventory():
        product.display_information()
        print(product.get_fulfilment_info())

    # LSP: Both products support inherited stock updates
    print("\n===== LSP TEST =====")

    for product in inventory.get_inventory():
        product.update_stock(8)
        print(product.find_product_name(), product.find_product_stock())

    # OBJECT RELATIONSHIP TEST
    print("\n===== OBJECT IDENTITY TEST =====")

    order1 = Order("ORD1")
    order2 = Order("ORD2")

    order1.add_order_line(physical, 2)
    order2.add_order_line(physical, 3)

    line1 = order1.order_lines[0]
    line2 = order2.order_lines[0]

    print("Same Product:", line1.product is line2.product)
    print("Same OrderLine:", line1 is line2)
    print("Product count: 1")
    print("OrderLine count:", len(order1.order_lines) + len(order2.order_lines))

    # Assertions
    assert line1.product is line2.product
    assert line1 is not line2
    assert physical.find_product_stock() == 8
    assert digital.find_product_stock() == 8

    print("\nAll OOP tests passed!")


# Run test when needed
test_oop()'''
