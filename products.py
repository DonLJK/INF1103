import typing
from abc import ABC, abstractmethod

from supplier import Supplier


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
