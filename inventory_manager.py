def print_menu(): #function to print the menu options for the inventory management system
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Exit")
    print("----------------------------")

def get_usr_input():
    option = input("Enter option: ")
    while option not in ['1', '2', '3', '4', '5']: #ensuring user input is valid and prompting user to enter a valid option if not
        print("Invalid option. Please select from 1-5.")
        option = input("Enter option: ")
    return option

def main():
    inventory = [
    {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15, "history": [15]},
    {"id": "P002", "name": "Mouse", "price": 25.5, "stock": 40, "history": [40]},
    {"id": "P003", "name": "Keyboard", "price": 45.0, "stock": 25, "history": [25]},
]  # list of product dictionaries
    print_menu()
    option = get_usr_input()


if __name__ == "__main__":
    main()