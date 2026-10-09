from database import get_connection
import mysql.connector
from decimal import Decimal,InvalidOperation

#---------------------------
# Add new Product
#--------------------------

def add_product():
    p_name = input("\nEnter Product name :").strip().capitalize()

    if not p_name :
        print("\nProduct Name cannot be empty!")
        return
    if p_name.isdigit():
        print("\nProduct Name cannot contain only digits!")
        return

    p_category = input("Category of Product :").strip().capitalize()
    
    if not p_category:
        print("\nProduct category cannot be empty!")
        return
    if p_category.isdigit():
        print("\nCategory cannot contain only digits!")
        return
    
    try:
        p_price = Decimal(input("Product price :"))
        if p_price <= 0:
            print("\nProduct Price must be greater than zero")
            return
        
    except InvalidOperation:
         print("\nPlear Enter price in digit")
         return
    try:
        p_quantity = int(input("Enter Quantity of product :"))

        if p_quantity <= 0:
                print("\nEnter Quantity Greater than Zero!")
                return
    except ValueError as e:
         print("\nPlear Enter Quantity in digit\n",e)
         return

    try:
        supplier_id = int(input("Enter Supplier Id :"))

        if not supplier_id:
             print("\nSupplier Cannot be empty!")
             return
    except ValueError as e:
         print("\nPlease Ensure Supplier Id is Digit")
         return

    #Insert Data Into Product Table 
    try:
        database = get_connection()
        cursor = database.cursor()

        qury="""
        SELECT supplier_id FROM inventory_system.suppliers
        WHERE supplier_id = %s
        """ 

        cursor.execute(qury,(supplier_id,))
        supplier = cursor.fetchone()

        if not supplier:
            print("\nSupplier Id not Found in Supplier data")
            return

        qury ="""
        INSERT INTO inventory_system.products(product_name,category,price,quantity,supplier_id)
        VALUES (%s,%s,%s,%s,%s)    
        """

        values = (p_name,p_category,p_price,p_quantity,supplier_id)

        cursor.execute(qury,values)

        product_id = cursor.lastrowid

        database.commit()
        print("\nProduct Add Sccuessfully!")
        print(f"Product Id : {product_id}")

    except mysql.connector.Error as error:
         database.rollback()
         print("\nDatabase Error..!\n",error)
    finally:
         if "cursor" in locals():
              cursor.close()
         if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# View All Orders
#-----------------------
def view_all_product():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT * FROM inventory_system.products
        ORDER BY product_id
        """

        cursor.execute(qury)

        products = cursor.fetchall()
        if not products:
            print("\nProducts Not Founds")
            return
        
        print("\n======= All Products =======\n")

        for product in products:
            print(f"""
    Product Id    :{product[0]}
    Product Name  :{product[1]}
    Category      :{product[2]}
    Price         :{product[3]}
    Quantity      :{product[4]}
    Supplier Id   :{product[5]}
    Create Time   :{product[6]}
        --------------------------------\n""")
    except mysql.connector.Error as error:
        print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()
    
#------------------------
# Search product By Name
#-----------------------

def search_product():
    product_name = input("\nEnter Product Name For Search :").strip().capitalize()

    if not product_name:
        print("\nProduct Name cannot be empty!")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT * FROM inventory_system.products
        WHERE product_name = %s
        """
        cursor.execute(qury,(product_name,))

        products = cursor.fetchall()
        if not products:
            print("\nProducts Not Founds")
            return
                
        print("\n======= Product Found =======\n")
        
        for product in products:
            print(f"""
    Product Id    :{product[0]}
    Product Name  :{product[1]}
    Category      :{product[2]}
    Price         :{product[3]}
    Quantity      :{product[4]}
    Supplier Id   :{product[5]}
    Create Time   :{product[6]}
                --------------------------------\n""")
    except mysql.connector.Error as error:
        print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#----------------------
# Update Product Name
#----------------------

def update_Pname(product):

    new_name = input("\nEnter New Product Name :").strip().capitalize()
    if not new_name :
        print("\nProduct Name cannot be empty!")
        return
    if new_name.isdigit():
        print("\nProduct Name cannot contain only digits!")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.products
        SET product_name = %s
        WHERE product_id = %s
        """
        cursor.execute(qury,(new_name,product[0]))
        database.commit()

        print("\nProduct Name Update Successfully!")
    except mysql.connector.Error as error:
            print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-------------------------
# Update Category
#------------------------
def update_category(product):

    new_category = input("\nEnter Updated Category :").strip().capitalize()
    if not new_category:
        print("\nProduct category cannot be empty!")
        return
    if new_category.isdigit():
        print("\nCategory cannot contain only digits!")
        return
        
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.products
        SET category = %s
        WHERE product_id = %s
        """
        cursor.execute(qury,(new_category,product[0]))
        database.commit()

        print("\nCategory Update Successfully!")
    except mysql.connector.Error as error:
            print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# Update Price
#----------------------
def update_price(product):

    try:
        new_price = Decimal(input("Enter Updated Product price :"))
        if new_price <= 0:
            print("\nProduct Price must be greater than zero")
            return
            
    except InvalidOperation:
        print("\nPlear Enter price in digit")
        return
   
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.products
        SET price = %s
        WHERE product_id = %s
        """
        cursor.execute(qury,(new_price,product[0]))
        database.commit()

        print("\nPrice Update Successfully!")
    except mysql.connector.Error as error:
            print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-------------------------
# Update Quantity
#------------------------
def update_quantity(product):

    try:
        new_quantity = int(input("Enter Updated Quantity of product :"))

        if new_quantity <= 0:
                print("\nEnter Quantity Greater than Zero!")
                return
    except ValueError:
         print("Plear Enter Quantity in digit")
   
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        UPDATE inventory_system.products
        SET quantity = %s
        WHERE product_id = %s
        """
        cursor.execute(qury,(new_quantity,product[0]))
        database.commit()

        print("\nQuantity Update Successfully!")
    except mysql.connector.Error as error:
            print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#--------------------------
#Update Supplier
#-------------------------

def update_supplier_id(product):

    try:
        new_supplier_id = int(input("Enter Updated Supplier Id :"))

        if not new_supplier_id:
             print("\nSupplier Cannot be empty!")
             return
    except ValueError as e:
         print("\nPlease Ensure Supplier Id is Digit")
         return
   
    try:
        database = get_connection()
        cursor = database.cursor()

        qury="""
        SELECT supplier_id FROM inventory_system.suppliers
        WHERE supplier_id = %s
        """ 
        
        cursor.execute(qury,(new_supplier_id,))
        supplier = cursor.fetchone()
        
        if not supplier:
            print("\nSupplier Id not Found in Supplier data")
            return

        qury = """
        UPDATE inventory_system.products
        SET supplier_id = %s
        WHERE product_id = %s
        """
        cursor.execute(qury,(new_supplier_id,product[0]))
        database.commit()

        print("\nSupplier Update Successfully!")
    except mysql.connector.Error as error:
            print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#----------------------
# Update product Menu
#---------------------

def update_product():
    try:
        product_id = int(input("\nEnter Product Id :"))

        if not product_id:
            print("\nProduct id cannot be empty!")
            return
    except ValueError as e:
        print("\nProduct Id only a number\n",e)
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury ="""
        SELECT product_id FROM inventory_system.products
        WHERE product_id = %s
        """

        cursor.execute(qury,(product_id,))
        product = cursor.fetchone()

        if not product:
            print("\nProduct not Found!")
            return
        while True:
            print("\n======= Update Products =======\n")
        
            print("1. Update Product Name")
            print("2. Update Product Category")
            print("3. Update Price")
            print("4. Update Quantity")
            print("5. Supplier Id")
            print("6. Back")
            
            try:
                choice = int(input("\nEnter The Choice :"))
                
                if not choice:
                    print("\nChoice Can't be empty!")
                    return
            except ValueError as e:
                print("\nPlease Enter choice in number \n",e)
                return
   

            if choice == 1:
                update_Pname(product)
            elif choice == 2:
                update_category(product)
            elif choice == 3:
                update_price(product)
            elif choice == 4:
                update_quantity(product)
            elif choice == 5:
                update_supplier_id(product)
            elif choice == 6:
                print("\nBack To main Menu")
                return
            else:
                print("\nInvalid Choice")
                return
    except mysql.connector.Error as error:
            print("\nDatabase Error..!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#----------------------
# Delete Product
#----------------------

def delete_product():
    try:
        try:   
            database = get_connection()
            cursor = database.cursor()  

            product_id =int(input("Enter Product id :"))
            if not product_id:
                print("\nProduct Id can't be empty!")
                return
             
        except ValueError as e:
            print("\nId must be a number\n",e)
            return
                
        qury ="""
            SELECT product_id FROM inventory_system.products
            WHERE product_id = %s
            """
        cursor.execute(qury,(product_id,))
        product =cursor.fetchone()
                
        if not product:
            print("\nProduct Not Exsist")
            return

        confirmation =input("\nAre You Sure to delete this Product from database (Yes / No) :").strip().lower()

        if confirmation != "yes":
            print("\nDelete Product Process Cancel!\n")
            return
            
        qury = """
            DELETE FROM inventory_system.products
            WHERE product_id = %s
            """
        cursor.execute(qury,(product_id,))

        database.commit()
        print("Product Delete Successfully..!")
        
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error..!\n",error)
    
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------
# Product Menu
#-----------------------

def product_menu():
    while True:
        print("\n*** Product Management ***\n")

        print("1. Add New Product")
        print("2. View All Products")
        print("3. Search Product By Name")
        print("4. Update Products By Id")
        print("5. Delete Product By Id")
        print("6. Exit")

        choice = int(input("\nEnter Choice :"))

        if choice == 1:
            add_product()
        elif choice == 2:
            view_all_product()
        elif choice == 3:
            search_product()
        elif choice == 4:
            update_product()
        elif choice == 5:
            delete_product()
        elif choice == 6:
            print("\nBack To Menu\n")
            return
        else:
            print("\nInvalid Choice")
            return

    
