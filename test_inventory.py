
import pytest
import csv

from oop_inv_sys_class2 import (
    Supplier,
    Physicalproduct,
    DigitalProduct,
    Inventory,
    Order,
    OrderLine,
    NoDiscount,
    PercentageDiscount,
    BulkDiscount,
    StudentDiscount,
    ProductFactory,
    get_positive_float,
    load_products,
)


# ==========================================
# FIXTURES
# ==========================================

@pytest.fixture
def supplier():
    return Supplier(1, "ABC Suppliers", "abc@gmail.com")


@pytest.fixture
def physical_product(supplier):
    return Physicalproduct(
        "P001", "Desk Lamp", 125.0, 10, supplier, 2.0
    )


@pytest.fixture
def inventory():
    return Inventory()


# ==========================================
# 1. STRATEGY PATTERN TESTS
# ==========================================

def test_no_discount(physical_product):
    order = Order("ORD001")
    order.add_order_line(physical_product, 2)

    assert order.calculate_total() == 250.0


def test_percentage_discount(physical_product):
    order = Order("ORD001", PercentageDiscount(10))
    order.add_order_line(physical_product, 2)

    assert order.calculate_total() == 225.0


def test_bulk_discount(physical_product):
    order = Order("ORD001", BulkDiscount(200, 20))
    order.add_order_line(physical_product, 2)

    assert order.calculate_total() == 230.0


def test_bulk_discount_below_threshold(physical_product):
    order = Order("ORD001", BulkDiscount(200, 20))
    order.add_order_line(physical_product, 1)

    assert order.calculate_total() == 125.0


def test_student_discount(physical_product):
    order = Order("ORD001", StudentDiscount())
    order.add_order_line(physical_product, 2)

    assert order.calculate_total() == 237.5


def test_change_discount_strategy(physical_product):
    order = Order("ORD001", BulkDiscount(200, 20))
    order.add_order_line(physical_product, 2)

    assert order.calculate_total() == 230.0

    order.set_discount(PercentageDiscount(10))

    assert order.calculate_total() == 225.0


def test_new_discount_strategy_without_changing_order(physical_product):
    # Demonstrates that Order accepts a new strategy
    # without needing modifications to the Order class.

    class TenDollarDiscount:
        def apply(self, total):
            return total - 10

    order = Order("ORD001", TenDollarDiscount())
    order.add_order_line(physical_product, 2)

    assert order.calculate_total() == 240.0


# ==========================================
# 2. ORDER AND ORDERLINE VALIDATION
# ==========================================

def test_orderline_subtotal(physical_product):
    line = OrderLine(physical_product, 2)

    assert line.calculate_subtotal() == 250.0


def test_orderline_rejects_zero_quantity(physical_product):
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        OrderLine(physical_product, 0)


def test_orderline_rejects_negative_quantity(physical_product):
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        OrderLine(physical_product, -1)


def test_order_rejects_quantity_above_stock(physical_product, capsys):
    order = Order("ORD001")
    order.add_order_line(physical_product, 20)

    assert len(order.order_lines) == 0
    assert "Insufficient stock!" in capsys.readouterr().out


def test_order_rejects_zero_quantity(physical_product, capsys):
    order = Order("ORD001")
    order.add_order_line(physical_product, 0)

    assert len(order.order_lines) == 0
    assert "Quantity must be greater than zero." in capsys.readouterr().out


# ==========================================
# 3. PRODUCT VALIDATION
# ==========================================

def test_product_rejects_zero_price(supplier):
    with pytest.raises(ValueError, match="Product price must be greater than zero"):
        Physicalproduct("P001", "Lamp", 0, 10, supplier, 2.0)


def test_product_rejects_negative_price(supplier):
    with pytest.raises(ValueError, match="Product price must be greater than zero"):
        Physicalproduct("P001", "Lamp", -10, 10, supplier, 2.0)


def test_product_rejects_negative_stock(supplier):
    with pytest.raises(ValueError, match="Product stock cannot be negative"):
        Physicalproduct("P001", "Lamp", 10, -1, supplier, 2.0)


def test_update_stock_rejects_negative_quantity(physical_product):
    with pytest.raises(ValueError, match="Product stock cannot be negative"):
        physical_product.update_stock(-5)


# ==========================================
# 4. FACTORY PATTERN TESTS
# ==========================================

def test_factory_creates_physical_product(supplier):
    product = ProductFactory.create(
        "physical", "P001", "Desk Lamp", 25.0, 10,
        supplier, weight=2.0
    )

    assert isinstance(product, Physicalproduct)
    assert product.find_product_name() == "Desk Lamp"
    assert product.find_product_price() == 25.0


def test_factory_creates_digital_product(supplier):
    product = ProductFactory.create(
        "digital", "D001", "Photo Editor", 49.90, 100,
        supplier, download_size="500MB"
    )

    assert isinstance(product, DigitalProduct)
    assert product.find_product_name() == "Photo Editor"
    assert product.get_download_size() == "500MB"


def test_factory_rejects_unknown_product_type(supplier):
    with pytest.raises(ValueError, match="Unknown Product type: service"):
        ProductFactory.create(
            "service", "S001", "Installation", 30.0, 5,
            supplier
        )


# ==========================================
# 5. INVENTORY TESTS
# ==========================================

def test_add_product_to_inventory(inventory, physical_product):
    inventory.add_product(physical_product)

    assert len(inventory.get_inventory()) == 1
    assert inventory.find_product("P001") == physical_product


def test_find_nonexistent_product(inventory):
    assert inventory.find_product("P999") is None


def test_get_total_stocks(inventory, physical_product):
    inventory.add_product(physical_product)

    assert inventory.get_total_stocks() == 10


def test_calculate_tax(inventory, physical_product):
    inventory.add_product(physical_product)

    assert inventory.calculate_tax() == 1.0


def test_update_inventory_stock(physical_product):
    physical_product.update_stock(20)

    assert physical_product.find_product_stock() == 20


# ==========================================
# 6. USER INPUT VALIDATION
# ==========================================

def test_get_positive_float_valid_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "12.50")

    result = get_positive_float("Enter price: ")

    assert result == 12.50


def test_get_positive_float_retries_invalid_input(monkeypatch, capsys):
    inputs = iter(["abc", "-5", "12.50"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_positive_float("Enter price: ")

    assert result == 12.50

    output = capsys.readouterr().out

    assert "Please enter a valid number" in output
    assert "Please enter a number greater than zero" in output


# ==========================================
# 7. CSV FILE LOADING TESTS
# ==========================================

def test_load_products_from_csv(tmp_path, inventory, supplier, capsys):
    csv_file = tmp_path / "products.csv"

    csv_file.write_text(
        "product_type,product_id,name,price,stock_quantity\n"
        "physical,P001,Desk Lamp,25.00,10\n"
        "digital,D001,Photo Editor,49.90,100\n"
        "service,S001,Installation,30.00,5\n"
        "physical,P002,Office Chair,abc,3\n"
        "physical,P003,Monitor Stand,39.50,7\n",
        encoding="utf-8"
    )

    load_products(str(csv_file), inventory, supplier)

    # 3 valid products should load.
    assert len(inventory.get_inventory()) == 3

    products = inventory.get_inventory()

    assert products[0].find_product_id() == "P001"
    assert products[1].find_product_id() == "D001"
    assert products[2].find_product_id() == "P003"

    output = capsys.readouterr().out

    assert "Unknown Product type: service" in output
    assert "could not convert string to float" in output.lower()
    assert "3 products loaded." in output
    assert "Load attempt finished." in output


def test_load_products_missing_file(inventory, supplier, tmp_path, capsys):
    missing_file = tmp_path / "missing.csv"

    load_products(str(missing_file), inventory, supplier)

    assert len(inventory.get_inventory()) == 0

    output = capsys.readouterr().out

    assert "Products file not found" in output
    assert "Load attempt finished." in output


# ==========================================
# 8. PRODUCT INFORMATION TESTS
# ==========================================

def test_physical_product_shipping_cost(physical_product):
    assert physical_product.calculate_shipping_cost() == 0.2


def test_physical_product_fulfilment(physical_product):
    assert physical_product.get_fulfilment_info() == (
        "Product requires physical shipping"
    )


def test_digital_product_fulfilment(supplier):
    product = DigitalProduct(
        "D001", "Photo Editor", 49.90, 100, supplier, "500MB"
    )

    assert product.get_fulfilment_info() == (
        "Product is delivered digitally"
    )
