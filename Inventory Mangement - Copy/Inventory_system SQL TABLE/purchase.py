from database import get_connection
import mysql.connector
from decimal import Decimal ,InvalidOperation


#-----------------------
# Create New Purchase
#---------------------

def create_purchase():
    try:
        supplier_id = int(input("Enter Supplier Id :"))

        if not supplier_id:
            print("\nSupplier Can't be Empty")
            return
    except ValueError as e:
        print("\nSupplier Id only be a number\n",e)
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT supplier_id FROM inventory_system.suppliers
        WHERE supplier_id = %s
        """

        cursor.execute(qury,(supplier_id,))
        supplier = cursor.fetchone()

        if not supplier:
            print("\nSupplier Can't found!")
            return

        qury = """
        INSERT INTO inventory_system.purchases(supplier_id)
        VALUES (%s)
        """

        cursor.execute(qury,(supplier_id,))
        database.commit()

        purchase_id = cursor.lastrowid

        print("\nPurchase Create Successfully!")
        print(f"Purchase Id : {purchase_id}")

    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# View All Purchase
#----------------------

def view_purchase():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT 
            p.purchase_id,
            s.supplier_name,
            p.total_amount,
            p.purchase_date
        FROM inventory_system.purchases as p
        JOIN 
        inventory_system.suppliers as s ON 
        p.supplier_id = s.supplier_id
        ORDER BY purchase_id
        """

        cursor.execute(qury)

        purchases = cursor.fetchall()

        if not purchases:
            print("\nPurchase Not Found!")
            return

        print("\n======= Purchase Found =======\n")

        for purchase in purchases:
            print(f"""
    Purchase Id       : {purchase[0]}
    Supplier Name     : {purchase[1]}
    Total Amount      : {purchase[2]}
    Purchase Date     : {purchase[3]}
    -----------------------------\n""") 
    except mysql.connector.Error as error:
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()
#---------------------
# Search Purchase
#--------------------

def search_purchase():
    try:
        purchase_id = int(input("\nEnter Purchase Id For Search Id :"))

        if not purchase_id:
            print("\nPurchase Id Can't be empty!")
            return
    except ValueError as e:
        print("\nPlease enter Id in Number\n",e)
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT 
            p.purchase_id,
            s.supplier_name,
            p.total_amount,
            p.purchase_date
        FROM inventory_system.purchases as p
        JOIN 
        inventory_system.suppliers as s ON 
        p.supplier_id = s.supplier_id
        WHERE purchase_id = %s
        """

        cursor.execute(qury,(purchase_id,))

        purchase = cursor.fetchone()

        if not purchase:
            print("\nPurchase Not Found!")
            return

        print("\n======= Purchase Detail =======\n")

        print(f"""
    Purchase Id       : {purchase[0]}
    Supplier Name     : {purchase[1]}
    Total Amount      : {purchase[2]}
    Purchase Date     : {purchase[3]}
    -----------------------------\n""") 
    except mysql.connector.Error as error:
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-------------------
# Delete Purchase
#------------------

def delete_purchase():
    try:
        try:   
            database = get_connection()
            cursor = database.cursor()  

            purchase_id =int(input("Enter Purchase id :"))
            if not purchase_id:
                print("\nPurchase Id can't be empty!")
                return
             
        except ValueError as e:
            print("\nId must be a number\n",e)
            return
                
        qury ="""
            SELECT purchase_id FROM inventory_system.purchases
            WHERE purchase_id = %s
            """
        cursor.execute(qury,(purchase_id,))
        product =cursor.fetchone()
                
        if not product:
            print("\nPurchase Not Exsist")
            return

        confirmation =input("\nAre You Sure to delete this Purchase from database (Yes / No) :").strip().lower()

        if confirmation != "yes":
            print("\nDelete Purchase Process Cancel!\n")
            return
        
        # Get product and quantity
        
        qury = """
        SELECT product_id , quantity 
        FROM purchase_details
        WHERE purchase_id = %s
        """
        
        cursor.execute(qury,(purchase_id,))
        detail = cursor.fetchall()
        
        for product_id , quantity in detail:
            qury = """
            SELECT product_id , quantity FROM 
            products WHERE product_id = %s
            """
            
            cursor.execute(qury,(product_id,))
            product = cursor.fetchone()
            
            if product:
                previous_quantity = product[1]
                new_quantity = previous_quantity - quantity
                
                if new_quantity < 0:
                    print("\nCannot Delete Purchase")
                    print("Stock would become negative")
                    database.rollback()
                    return
                
                qury = """
                UPDATE products
                SET quantity = %s
                WHERE product_id = %s"""
                
                cursor.execute(qury,(new_quantity,product_id))
                
                #add stock history
                
                qury = """
                INSERT INTO stock_history(product_id,transcation_type,quantity, previous_quantity,new_quantity)
                VALUES (%s,%s,%s,%s,%s)
                """   
                values = (product_id,"Stock IN",quantity,previous_quantity,new_quantity)
                        
                cursor.execute(qury,values)
                
        
        qury = """
            DELETE FROM inventory_system.purchases
            WHERE purchase_id = %s
            """
        cursor.execute(qury,(purchase_id,))

        database.commit()
        print("Purchase Delete Successfully..!")
        
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error..!\n",error)
    
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#--------------------
# Purchase Details 
#------------------

def purchase_detail():
    try:
        purchase_id = int(input("\nEnter Purchase Id : "))

        if not purchase_id :
            print("\nPurchase Id Can't be empty!")
            return

        product_id = int(input("Enter Product Id : "))

        if not product_id:
            print("\nProduct Id Can't be empty!")
            return

        quantity = int(input("Enter Product Quantity : "))

        if quantity <= 0:
            print("\nProduct Quantity must be greater than 0!")
            return
   
    except ValueError as e:
        print("\nPlease Enter Valid Number !\n",e)
        return
    
    try:
        unit_price = Decimal(input("Enter Unit Price of Product : "))

        if unit_price <= 0:
            print("\nUnit Price must be greater than 0!")
            return
    except InvalidOperation:
        print("\nPlease enter valid price !")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT purchase_id FROM inventory_system.purchases
        WHERE purchase_id = %s
        """
        cursor.execute(qury,(purchase_id,))

        purchase = cursor.fetchone()

        if not purchase:
            print("\nPurchase Id not Found!")
            return

        qury = """
        SELECT product_id , quantity FROM inventory_system.products
        WHERE product_id = %s
        """

        cursor.execute(qury,(product_id,))

        product = cursor.fetchone()

        if not product:
            print("\nProduct Id not Found!")
            return
                
        qury = """
        INSERT INTO inventory_system.purchase_details(purchase_id,product_id,quantity,unit_price)
        VALUES (%s,%s,%s,%s)
        """

        values = (purchase_id,product_id,quantity,unit_price)

        cursor.execute(qury,values)
        
        # Add Stock in product Table
        previous_quantity = product[1]
        new_quantity = previous_quantity + quantity
        
        qury = """
        UPDATE products
        SET quantity = %s
        WHERE product_id = %s
        """
        
        cursor.execute(qury,(new_quantity,product_id))
        
        #Stock History
        
        qury = """
        INSERT INTO stock_history(product_id,transcation_type,quantity, previous_quantity,new_quantity)
        VALUES (%s,%s,%s,%s,%s)
        """
        
        values = (product_id,"Stock IN",quantity,previous_quantity,new_quantity)
        
        cursor.execute(qury,values)


        database.commit()

        update_purchase_amount(purchase_id,cursor,database)

        print("\nPurchase Details Added Successfully!")
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#---------------------
# Update Purchase Total Amount 
#---------------------

def update_purchase_amount(purchase_id,cursor,database):

    qury = """
    SELECT SUM(quantity * unit_price) FROM inventory_system.purchase_details
    WHERE purchase_id = %s
    """

    cursor.execute(qury,(purchase_id,))

    result = cursor.fetchone()

    total_amount = result[0] if result [0] else 0

    qury = """
    UPDATE inventory_system.purchases
    SET total_amount = %s
    WHERE purchase_id = %s
    """

    cursor.execute(qury,(total_amount,purchase_id))

    database.commit()


#----------------------
# purchase Menu
#---------------------

def purchase_menu():
    while True:
        print("\n*** Purchase Management ***\n")

        print("1. Create New Purhase")
        print("2. Create Purchase Detail")
        print("3. View All Purchase")
        print("4. Search Purchase By Id")
        print("5. Delete Purchase")
        print("6. Exit ")
        try:
            choice = int(input("\nEnter chocie :"))

            if not choice:
                print("\nkinldy enter any number ")
                return
        except ValueError as e:
            print("\nPlease Enter choice in numbers\n",e)
            return

        if choice == 1:
            create_purchase()
        elif choice == 2:
            purchase_detail()
        elif choice == 3:
            view_purchase()
        elif choice == 4:
            search_purchase()
        elif choice == 5:
            delete_purchase()
        elif choice == 6:
            print("\nExit from Purchase Menu\n")
            break
        else:
            print("\nInvalid Choice")
            return

    
