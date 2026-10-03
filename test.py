stocks = {
    "uid": []
}

def add_product(item_name, qty):
    stocks["uid"].append({
        "item name: ": item_name, 
        "Quantity: ": qty
    })
    pass

def update_stock():
    pass

def search_product(): 
    pass

def display_all():
    pass


itemname = input("enter item name")
qty = input("qty?: ")
add_product(itemname, qty)

print(stocks)