from products import Product


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
