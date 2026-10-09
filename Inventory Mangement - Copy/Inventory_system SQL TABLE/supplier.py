from database import get_connection
import mysql.connector

#------------------------
# Add New Suppliers
#-----------------------

def add_supplier():
    s_name  =input("Enter Supplier Name :").strip().capitalize()

    if not s_name:
        print("\nSupplier name cannot be empty!")
        return
    if s_name.isdigit():
        print("\nSupplier Name Cannot contain only digit!")
        return
    
    s_phone =input("Enter Supplier Contact Number :").strip()

    if len(s_phone) != 11 or not s_phone.isdigit():
        print("\nError..!")
        print("Phone number must be 11 digits")
        return

    s_email =input("Enter Email :").strip().lower()

    if "@" not in s_email or "." not in s_email.split("@")[-1]:
        print("\nInvalid Email")
        print("@ & . must in email")
        return

    s_address = input("Enter Supplier Address :").strip().capitalize()

    if not s_address:
        print("\nAddress Cannot be empty!")
        return
    if s_address.isdigit():
            print("\nSupplier address Cannot contain only digit!")
            return
    try:
        # Data base 
        database = get_connection()
        cursor = database.cursor()

        qury = """
        INSERT INTO inventory_system.suppliers(supplier_name,phone,email,address)
        VALUES (%s,%s,%s,%s)
        """
        values = (s_name,s_phone,s_email,s_address)

        cursor.execute(qury,values)

        database.commit()
        
        print("\nSupplier Add Successfully...!")
        print(f"\nSupplier Id is : {cursor.lastrowid}")

    except mysql.connector.Error as error :
        database.rollback()
        print("\nDatabase Error..!",error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# View All Suppliers
#------------------------

def view_all_supplier():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury= """
        SELECT *FROM inventory_system.suppliers
        ORDER BY supplier_id 
        """

        cursor.execute(qury)

        suppliers = cursor.fetchall()

        if not suppliers:
            print("\nSuppliers not Found..!")
            return

        print("\n======= All Supplier Data =======\n")
        for supplier in suppliers:
            print(f"""
        Supplier ID    : {supplier[0]}
        Supplier Name  : {supplier[1]}
        Phone Number   : {supplier[2]}
        Email Address  : {supplier[3]}
        Address        : {supplier[4]}
        --------------------------------\n""")

    except mysql.connector.Error as error:
        print("\nDatabase Error...!",error)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'database' in locals() and database.is_connected():
            database.close()

#--------------------
# Search Supplier by name
#--------------------

def search_supplier():
    name = input("\nEnter Supplier Name :").strip()

    if not name:
        print("\nSupplier Cannot be Empty!")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT * FROM inventory_system.suppliers
        WHERE LOWER(supplier_name) LIKE LOWER(%s)
        """
        cursor.execute(qury,(f"%{name}%",))

        suppliers = cursor.fetchall()

        if not suppliers:
            print("\nSupplier Not Found By Name")
            return
        print("\n======= Supplier Found =======\n")
        for supplier in suppliers:
            print(f"""
    Supplier ID    : {supplier[0]}
    Supplier Name  : {supplier[1]}
    Phone Number   : {supplier[2]}
    Email Address  : {supplier[3]}   
    Address        : {supplier[4]}
    --------------------------------\n""")
    except mysql.connector.Error as error:
        print("Database Error...!",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------------    
#Update Supplier Phone number 
#-----------------------------

def update_phone(supplier):
    new_phone = input("Enter New Phone Number : ").strip()
    
    if len(new_phone) != 11 or not new_phone.isdigit():
        print("\nError..!")
        print("Phone number must be 11 digits")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.suppliers
        SET phone = %s
        WHERE supplier_id = %s
        """
        cursor.execute(qury,(new_phone,supplier[0]))

        database.commit()
        print("Phone Number Update Successfully..!")

    except mysql.connector.Error as error:
        print("Database Error..!",error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#--------------------------
# Update Email 
#--------------------------

def update_email(supplier):
    
    new_email = input("\nEnter New Email : ").strip().lower()

    if "@" not in new_email or "." not in new_email.split("@")[-1]:
        print("\nInvalid Email")
        print("@ & . must in email")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.suppliers
        SET email = %s
        WHERE supplier_id = %s
        """
        cursor.execute(qury,(new_email,supplier[0]))

        database.commit()
        print("Email Update Successfully..!")

    except mysql.connector.Error as error:
        print("Database Error..!",error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#---------------------
#Update Address 
#--------------------

def update_address(supplier):
    new_address = input("\nEnter New Address : ").strip().capitalize()

    if not new_address:
        print("\nAddress Cannot be empty!")
        return
    if new_address.isdigit():
        print("\nSupplier address Cannot contain only digit!")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.suppliers
        SET address = %s
        WHERE supplier_id = %s
        """
        cursor.execute(qury,(new_address,supplier[0]))

        database.commit()
        print("Address Update Successfully..!")

    except mysql.connector.Error as error:
        print("Database Error..!",error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()
    


#--------------------------
# Supplier Update menu
#--------------------------

def update_supplier():
    try:
        database = get_connection()
        cursor = database.cursor()
        try:      
            supplier_id =int(input("Enter Supplier id :"))
        except ValueError as e:
            print("\nId must be a number\n",e)
            return
        
        qury ="""
            SELECT supplier_id FROM inventory_system.suppliers
            WHERE supplier_id = %s
            """
        cursor.execute(qury,(supplier_id,))
        supplier =cursor.fetchone()
        
        if not supplier:
            print("\nSupplier Not Exsist")
            return

        print("\n====== Update Supplier Profile ======\n")

        print("1. Update Phone")
        print("2. Update Email")
        print("3. Update Address")
        print("4. Exit")
        try:
            choice = int(input("\nEnter The choice :"))
        except ValueError:
            print("\nPlz enter choice in given numbers")
            return

        if choice == 1:
            update_phone(supplier)
        elif choice == 2:
            update_email(supplier)
        elif choice == 3:
            update_address(supplier)
        elif choice == 4:
            print("\nBack to Menu")
            return
        else:
            print("\nEnter Valid Choice")
    except mysql.connector.Error as error:
        print("\nDatabase Error..!",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-------------------------
#Close Or Del Supplier
#------------------------
def delete_supplier():
    try:
        try:   
            database = get_connection()
            cursor = database.cursor()  

            supplier_id =int(input("Enter Supplier id :"))
        except ValueError as e:
            print("\nId must be a number\n",e)
            return
                
        qury ="""
            SELECT supplier_id FROM inventory_system.suppliers
            WHERE supplier_id = %s
            """
        cursor.execute(qury,(supplier_id,))
        supplier =cursor.fetchone()
                
        if not supplier:
            print("\nSupplier Not Exsist")
            return

        confirmation =input("\nAre You Sure to delete this supplier from database (Yes / No) :").strip().lower()

        if confirmation != "yes":
            print("\nDelete Supplier Process Cancel!\n")
            return
            
        qury = """
            DELETE FROM inventory_system.suppliers
            WHERE supplier_id = %s
            """
        cursor.execute(qury,(supplier_id,))

        database.commit()
        print("Supplier Delete Successfully..!")
        
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error..!\n",error)
    
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()


#-------------------------------
#Supplier Information 
#-------------------------------

def supplier_information():
    while True:
        print("\n*** Supplier Management ***\n")
        
        print("1. Add New Supplier")
        print("2. View All Supplier")
        print("3. Search Supplier By Name")
        print("4. Update Supplier By Id")
        print("5. Delete Supplier By Id")
        print("6. Exit\n")

        try:
            choice = int(input("\nEnter The Choice :"))
            
            if not choice:
                print("\nChoice Can't be empty!")
                return
        except ValueError as e:
            print("\nPlease Enter choice in number \n",e)
            return


        if choice == 1:
            add_supplier()
        elif choice == 2:
            view_all_supplier()
        elif choice == 3:
            search_supplier()
        elif choice == 4:
            update_supplier()
        elif choice == 5:
            delete_supplier()
        elif choice == 6:
            print("Back to Main Menu")
            return
        else:
            print("\nInvalid Choice")
            return

