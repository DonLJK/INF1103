inv = 0
rejected_entry = 0

while(inv < 510):
    val = input("Enter Stock quantity: ")

    if val == "quit":
        print("Inventory = :",  inv)
        print("Rejected Entries = :", rejected_entry)
        break
    
    elif val.isdigit() != True:
        print("Value has been rejected")
        rejected_entry += 1
        continue
    
    elif int(val) < 0:
        print("Value is invaild")
        print("Value will remain at: ", inv)
        continue

    else:
        inv += int(val)
        print("Current Inventory: ", inv)

        if inv == 500:
            print("Inventory limit reached")
            print("inventory overflow: ", inv - 500)
        elif int(inv) > 500: 
            print("Inventory overflow: ", inv - 500)
            print("programme closing")
            break 
                #print("Error: Inventory limit exceeded")
                #overflow = inv - 500
                #print("Overflow amount: ", overflow)
                