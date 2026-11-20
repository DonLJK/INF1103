from discounts import DiscountStrat, NoDiscount
from inventory import Inventory
from products import Product


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
