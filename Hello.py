username = input("Enter your username: ")
age = int(input("Enter your age: "))
category = input("Enter your category (e.g., student, professional): ")

print("\nInstagram Profile")
print("=======================")
print("username: ", username)
print("age: ", age)
print("category: ", category)

if age>40 and category == "fun":
    print("You are eligible for the fun category!")