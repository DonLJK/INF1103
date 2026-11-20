class Supplier:
    def __init__(self, Supplier_id: int, name: str, email: str) -> None:
        self.supplier_id:int = Supplier_id
        self.supplier_name:str = name
        self.supplier_email:str = email
        return

    def display_information(self) -> None:
        return print(f"Supplier ID: {self.supplier_id}\nSupplier Name: {self.supplier_name}\nSupplier Email: {self.supplier_email}")
