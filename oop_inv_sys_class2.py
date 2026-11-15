import _io
import io
import csv
import math
import json
from abc import ABC, abstractmethod
import typing
class DiscountStrat(ABC):
    @abstractmethod
    def apply(self, total:float) -> float:
        pass

class NoDiscount(DiscountStrat):
    def apply(self, total:float) -> float:
        return total

class PercentageDiscount(DiscountStrat):
    def __init__(self, percentage: float) -> None:
        self.percentage: float = percentage
    def apply(self, total: float) -> float:
        return total * (1-self.percentage/100)

class BulkDiscount(DiscountStrat):
    def __init__(self, threshold:float, discount:float) -> None:
        self.threshold: float = threshold
        self.discount: float = discount

    def apply(self, total: float) -> float:
        if total >= self.threshold: 
            return total - self.discount
        return total

class StudentDiscount(DiscountStrat):
    def apply(self, total: float) -> float:
        return total * 0.95


class Supplier:
    def __init__(self, Supplier_id: int, name: str, email: str) -> None:
        self.supplier_id:int = Supplier_id
        self.supplier_name:str = name
        self.supplier_email:str = email
        return

    def display_information(self) -> None:
        return print(f"Supplier ID: {self.supplier_id}\nSupplier Name: {self.supplier_name}\nSupplier Email: {self.supplier_email}")


class Product(ABC):#Used Source-Action apply all annotation to save time for subsequent singatures
    def __init__ (self, productid:int | str, name:str, price:float, stock:int, supplier: Supplier) -> None:
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")

        if stock < 0:
            raise ValueError("Product stock cannot be negative.")
        self.__productid: int = productid
        self.__productname: str = name
        self.__productprice: float = price
        self.__productstock: int = stock
        self.supplier: Supplier = supplier


    def update_stock(self, quantity:int) -> None:
        if quantity < 0:
            raise ValueError("Product stock cannot be negative.")
        self.__productstock: int = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__productid} | Name: {self.__productname} | Price:  {self.__productprice} | Stock: {self.__productstock}")
        return 

    def find_product_id(self) -> str:
        return self.__productid

    def find_product_name(self) -> str:
        return self.__productname

    def find_product_price(self) -> float:
        return self.__productprice

    def find_product_stock(self) -> int:
        return self.__productstock

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def display_supply_info(self) -> None:
        self.supplier.display_information()

    def get_supply_info(self) -> tuple[int, str, str]:
        return self.supplier.supplier_id, self.supplier.supplier_name, self.supplier.supplier_email

class CanBeShipped(ABC):
    @abstractmethod
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

    def find_product(self, id: str | int) -> Product|None:
        for items in self.__inventory:
            if str(items.find_product_id()) == str(id):
                return items
        return None 

    def get_next_id(self, prefix: str) -> str:
        numbers = []
        for product in self.__inventory:
            product_id = str(product.find_product_id())
            suffix = product_id.removeprefix(prefix)
            if suffix.isdigit():
                numbers.append(int(suffix))

        return f"{prefix}{max(numbers, default=0) + 1:03d}"

    def get_inventory(self) -> list[Product]:
        return self.__inventory.copy()

    def get_total_stocks(self) -> int:
        total: int = sum(items.find_product_stock() for items in self.__inventory)
        return total

    def check_storage_space(self, total_stocks:int , qty:int) -> int:
        new_total: int = total_stocks + int(qty)
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

    def remove(self, item_id: int) -> None:
        for product in self.__inventory:
            if product.find_product_id() == item_id:
                self.__inventory.remove(product)
                print("Product Removed")
                return
    print("Product not found")


class OrderLine: 
    def __init__(self, product:Product, qty: int) -> None:
        if qty <= 0:
                    raise ValueError("Quantity must be greater than 0")
        self.product: Product = product
        self.quantity: int = qty

    def calculate_subtotal(self) -> float:
        return self.product.find_product_price() * self.quantity


class Order:
    def __init__(self, order_id: str, discount: DiscountStrat = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrat = discount if discount is not None else NoDiscount()

    def set_discount(self, discount: DiscountStrat) -> None:
        self.discount: DiscountStrat = discount

    def calculate_total(self) -> float:
        total_value: float = 0.0

        for order_line in self.order_lines:
            total_value += order_line.calculate_subtotal()
            
        return self.discount.apply(total_value)

    def add_order_line(self, product: Product, quantity: int) -> None:
            if quantity <= 0:
                print("Quantity must be greater than zero.")
                return
    
            if quantity > product.find_product_stock():
                print("Insufficient stock!")
                return
    
            order_line: OrderLine = OrderLine(product, quantity)
            self.order_lines.append(order_line)

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
                pid: str = input("Enter Product ID: ").strip()
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

class ProductFactory:
    @staticmethod
    def create(product_type:str , product_id:int , product_name:str, product_price:float, product_stock:int, supplier:Supplier, **kwargs) -> Physicalproduct | DigitalProduct:
        if product_type == "physical":
            return Physicalproduct(product_id, product_name, product_price, product_stock, supplier, kwargs["weight"])
        elif product_type == "digital":
            return DigitalProduct(product_id, product_name, product_price, product_stock, supplier, kwargs["download_size"])
        else:
            raise ValueError(
                f"Unknown Product type: {product_type}"
            )

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
        print("9. Import products from csv file")

    def get_user_input() -> int:
        while True:
            try:
                return int(input("\nSelect an Option: "))
            except ValueError:
                print("Please enter a number.")

    def display_options() -> None:
        print("1. Physical product")
        print("2. Digital product")

def get_valid_input() -> tuple[float, int] | None:
    while True:
        qty_text: str = input("Enter stock quantity (or 'quit' to cancel): ").strip()

        if qty_text.lower() == "quit":
            return None

        try:
            quantity = int(qty_text)
            if quantity < 0:
                raise ValueError
        except ValueError:
            print("Stock must be a whole number of 0 or more.")
            continue

        try:
            price = float(input("Price: "))
        except ValueError:
            print("Enter a valid price.")
            continue

        if not math.isfinite(price) or price <= 0:
            print("Price must be a finite number greater than zero.")
            continue

        return price, quantity

def get_positive_float(prompt: str) -> float:

    while True:
        try:
            value = float(input(prompt))

            if not math.isfinite(value) or value <= 0:
                print("Please enter a number greater than zero.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
        
    
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
        try:
            item: Physicalproduct | DigitalProduct = ProductFactory.create(
                product_type,
                i["order_id"],
                i["item_name"],
                i["item_price"],
                i["qty"],
                supplier,
                weight=i["weight"]
            ) if product_type == "physical" else ProductFactory.create(
                product_type,
                i["order_id"],
                i["item_name"],
                i["item_price"],
                i["qty"],
                supplier,
                download_size=i["download_size"]
            )
        except ValueError as error:
            print(f"Skipping product: {error}")
            continue

        inventory.store_product(item)
    return inventory

def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    product_type = row["product_type"]
                    product_id = row["product_id"]
                    name = row["name"]
                    price = float(row["price"])
                    stock = int(row["stock_quantity"])
                    if product_type == "physical":
                        product = ProductFactory.create("physical", product_id, name, price, stock, supplier, weight=1.0)
                    elif product_type == "digital":
                        product = ProductFactory.create("digital", product_id, name, price, stock, supplier, download_size="Unknown")
                    else:
                        product = ProductFactory.create(product_type, product_id, name, price,stock, supplier)
                    inventory.store_product(product)
                    loaded += 1

                except ValueError as error:
                    print(f"Skipping product: {error}")

                except KeyError as error:
                    print(f"Skipping invalid row: missing {error}")

        print(f"{loaded} products loaded.")

    finally:
        print("Load attempt finished.")

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
my_inventory: Inventory = load_inventory()
customer_order = OrderManager(my_inventory)
while True:
    try:
        choice = Menu.get_user_input()
    except UnboundLocalError:
        print("Please Select 1-6")
        continue
    match choice:
        case 1:
            print("\n====Displaying Inventory====\n")
            my_inventory.display_all()

        case 2:
            print("==== ADD PRODUCT ====")
            Menu.display_options()
            u_choice = Menu.get_user_input()
            if u_choice not in (1, 2):
                print("Please choose 1 or 2.")
                continue
            prefix = "P" if u_choice == 1 else "D"
            product_id = my_inventory.get_next_id(prefix)
            print("Product ID:", product_id)
            prod_name: str = input("Product name (or 'quit' to cancel): ").strip()
            if prod_name.lower() == "quit":
                continue
            if not prod_name:
                print("Product name cannot be empty.")
                continue

            result: tuple[float, int] | None = get_valid_input()
            if result is None:
                continue

            price, quantity = result

            total = my_inventory.get_total_stocks()
            new_total = my_inventory.check_storage_space(total, quantity)
            if new_total == total and quantity > 0:
                continue

            try:
                if u_choice == 1:
                    weight: float = get_positive_float("Enter Product Weight (kg): ")
                    if not math.isfinite(weight):
                        print("Weight must be a finite number.")
                        continue

                    new_item: Physicalproduct | DigitalProduct = ProductFactory.create(
                        "physical", product_id, prod_name, price, quantity,
                        supplier, weight=weight
                    )
                else:
                    download_size: str = input("Enter Download size: ").strip()
                    if not download_size:
                        print("Download size cannot be empty.")
                        continue

                    new_item: Physicalproduct | DigitalProduct = ProductFactory.create(
                        "digital", product_id, prod_name, price, quantity,
                        supplier, download_size=download_size
                    )

            except ValueError as error:
                print(f"Could not add product: {error}")
                continue

            my_inventory.add_product(new_item)

        case 3:
            print("=====Update Product====")
            pid = input("Product ID: ").strip()
            item: Product | None = my_inventory.find_product(pid)
            if item is None:
                print("Product Not found")
            elif item is not None:
                print("==Product Found!==")
                item.display_information()
                qty: str = input("New Stock value: ")
                total: int = my_inventory.get_total_stocks()
                new_total: int = my_inventory.check_storage_space(total, qty)
                if new_total == total:
                            continue
                item.update_stock(int(qty))
                print("Stock updated!")

        case 4:
            print("====Search Product====")
            pid = input("Product ID: ")
            item = my_inventory.find_product(pid)
            if item is None: 
                print("Product Not Found")
            elif item is not None:
                print("==Product Found!==")
                item.display_information()
            
        case 5:
            generate_and_save_report(my_inventory, error_count, my_inventory.calculate_tax(), customer_order.orders)

        case 6:
            pid = input("Product ID: ")
            my_inventory.remove(pid)

        case 7: #Creates customer order 
            customer_order.create_order()

        case 8:
            er_count: int = error_count
            tax: float =  my_inventory.calculate_tax()
            generate_and_save_report(my_inventory, error_count, my_inventory.calculate_tax(), customer_order.orders)
            print("Saving inventory before exit...")
            print("Inventory Saved successfully\n\n")
            print("Program Terminated")
            break

        case 9:
            load_products("products.csv", my_inventory, supplier)

