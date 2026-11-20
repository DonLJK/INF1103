import csv
import math
import json

from discounts import DiscountStrat, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount
from supplier import Supplier
from products import Product, CanBeShipped, Physicalproduct, DigitalProduct
from inventory import Inventory
from orders import OrderLine, Order, OrderManager
from product_factory import ProductFactory
from menu import Menu
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

def main():
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

if __name__  == "__main__": 
    main()