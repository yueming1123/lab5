import json #used to load and save the inventory
import os #used to find the folder this script is in
import math #used to reject nan/inf when reading prices

def print_banner():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

def print_menu(): #function to print the menu options for the inventory management system
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

def get_usr_input():
    option = input("\nEnter option: ")
    while option not in ['1', '2', '3', '4', '5', '6']: #ensuring user input is valid and prompting user to enter a valid option if not
        print("Invalid option. Please select from 1-6.")
        option = input("\nEnter option: ")
    return option

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products in inventory.")
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | "
              f"Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)

def find_product(inventory, product_id):
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None

def add_product(inventory, product_id, name, price, stock):
    if find_product(inventory, product_id):  # product IDs must be unique
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "history": [stock],  # history of all stock changes for this product
    })
    return True

def update_stock(inventory, product_id, new_stock): #function to update the stock of a product and record the change in its history
    product = find_product(inventory, product_id)
    if product is None: #nothing to update if the product does not exist
        return None
    change = new_stock - product["stock"]
    product["stock"] = new_stock
    product.setdefault("history", []).append(change) #record the stock change in the product's history
    return product

def search_product(inventory, product_id): #function to search for a product by its ID and display its details if found
    product = find_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return None
    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)
    return product

def get_text(prompt): #function to get a non-empty string from the user, ensuring it is valid
    text = input(prompt).strip()
    while not text: #reject empty input and prompt again
        print("This field cannot be empty.")
        text = input(prompt).strip()
    return text

def get_number(prompt, number_type): #function to get a number from the user, ensuring it is valid and non-negative
    while True:
        try:
            value = number_type(input(prompt).strip())
        except ValueError: #catching invalid input and prompting user to enter a valid number
            print("Please enter a valid number.")
            continue
        if value < 0 or not math.isfinite(value): #reject negative numbers
            print("Please enter a non-negative number.")
            continue
        return value

def load_inventory(): #load the inventory from a JSON file, or create an empty inventory if the file does not exist
    try:
        with open("inventory.json", "r") as file:
            inventory = json.load(file)
        print("\ninventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    except FileNotFoundError: #file does not exist yet, so create it with an empty inventory
        print("\ninventory.json not found. Starting with an empty inventory.")
        with open("inventory.json", "w") as file:
            json.dump([], file, indent=4)
        return []
    except json.JSONDecodeError: #file exists but is empty or not valid JSON
        print("\ninventory.json found, but it is empty or invalid. Starting with an empty inventory.")
        return []


def save_inventory(inventory): #save the current inventory to a JSON file
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__))) #work in the script's own folder, where inventory.json is
    print_banner()
    inventory = load_inventory()  # list of product dictionaries
    print_menu()
    while True: #keep showing options until the user enters 6
        option = get_usr_input()
        if option == '1':
            display_all(inventory)
        elif option == '2':
            print("\nAdd New Product")
            product_id = get_text("Product ID: ")
            if find_product(inventory, product_id): #check before asking for the rest of the details
                print("\nA product with that ID already exists.")
            else:
                name = get_text("Product Name: ")
                price = get_number("Price: ", float)
                stock = get_number("Stock Quantity: ", int)
                add_product(inventory, product_id, name, price, stock)
                print("\nProduct added successfully!")
        elif option == '3':
            print("\nUpdate Stock")
            product = find_product(inventory, get_text("Enter Product ID: "))
            if product is None:
                print("\nProduct not found.")
            else:
                print("\nProduct Found:")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                new_stock = get_number("\nNew Stock Quantity: ", int)
                update_stock(inventory, product["id"], new_stock)
                print("\nStock updated successfully!")
        elif option == '4':
            print("\nSearch Product")
            search_product(inventory, get_text("Enter Product ID: "))
        elif option == '5':
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif option == '6':
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break


if __name__ == "__main__":
    main()