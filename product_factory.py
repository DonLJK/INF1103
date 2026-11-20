from products import DigitalProduct, Physicalproduct
from supplier import Supplier


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
