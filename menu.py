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
