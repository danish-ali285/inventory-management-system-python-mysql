from supplier import supplier_information
from product import product_menu
from purchase import purchase_menu
from stock import stock_menu
from sale import sale_menu
from report import report_menu

while True:
    print("\n*********************************\n")
    print("   INVENTORY MANAGEMENT SYSTEM    ")
    print("\n*********************************\n")

    print("1. Supplier Management ")
    print("2. Products Management ")
    print("3. Purchase Management")
    print("4. Stock Management")
    print("5. Sale Management")
    print("6. Reports Management")
    print("7. Exit From Inventory Management System")

    try:
        choice = int(input("\nEnter The Choice :"))
            
        if not choice:
            print("\nChoice Can't be empty!")
            break
    except ValueError as e:
        print("\nPlease Enter choice in number \n",e)

    if choice == 1:
        supplier_information()
    elif choice == 2:
        product_menu()
    elif choice == 3:
        purchase_menu()
    elif choice == 4:
        stock_menu()
    elif choice == 5:
        sale_menu()
    elif choice == 6:
        report_menu()
    elif choice == 7:
        print("\nExit From Inventory Management System\n")
        break
    else:
        print("\nInvalid Choice")
    