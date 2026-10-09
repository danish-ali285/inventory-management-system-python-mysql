from database import get_connection
import mysql.connector
from decimal import Decimal,InvalidOperation

def sale_create():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        INSERT INTO inventory_system.sales()
        VALUES()
        """
        cursor.execute(qury)

        database.commit()

        sale_id = cursor.lastrowid

        print("\nSale create successfully!")
        print("Your Sale Id : ",sale_id,"\n")

    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error ! \n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#----------------------
# Sale Detail 
#----------------------

def sale_detail():
    try:
        sale_id = int(input("\nEnter Sale Id :"))

        if not sale_id:
            print("\nSale Id can't be empty!")
            return
    except ValueError as e:
        print("\nPlease enter valid number\n",e)
        return
    
    try:
        product_id = int(input("Enter product Id :"))

        if not product_id:
            print("\nProduct Id can't be empty!")
            return
    except ValueError as e:
        print("\nPlease enter valid number\n",e)
        return
    try:
        quantity = int(input("Enter Quantity :"))

        if quantity <= 0:
            print("\nQuantity must be greater than zero")
            return
    except ValueError as e :
        print("\nPlease enter valid quantity")
        return

    try:
        unit_price = Decimal(input("Enter Unit Price :"))

        if unit_price <= 0:
            print("\nPrice must be graeter than zero")
            return
    except InvalidOperation:
        print("\nPlease enter valid price")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT sale_id FROM inventory_system.sales
        WHERE sale_id = %s
        """

        cursor.execute(qury,(sale_id,))

        sale = cursor.fetchone()

        if not sale:
            print("\nSale Id not found!")
            return

        qury = """
        SELECT product_id,quantity FROM inventory_system.products
        WHERE product_id = %s
        """

        cursor.execute(qury,(product_id,))

        product = cursor.fetchone()

        if not product:
            print("\nProduct Id not Found!")
            return

        current_stock = product[1]

        if quantity > current_stock:
            print("\n!Insufficient Balance")
            print("Current Stock :",current_stock)
            return

        qury = """
        INSERT INTO sale_details(sale_id,product_id,quantity,unit_price)
        VALUES (%s,%s,%s,%s)
        """

        values = (sale_id,product_id,quantity,unit_price)

        cursor.execute(qury,values)

        update_sale_total(sale_id,cursor,database)

        #------------------------
        # Remove Stock From Inventory
        #------------------------
        new_stock = current_stock - quantity

        qury = """
        UPDATE inventory_system.products
        SET quantity = quantity - %s
        WHERE product_id = %s
        """

        cursor.execute(qury,(quantity,product_id))

        qury = """
        INSERT INTO inventory_system.stock_history
        (product_id,transcation_type,quantity,previous_quantity,new_quantity)
        VALUES (%s,%s,%s,%s,%s)
        """
        values = (product_id,"Stock OUT",quantity,current_stock,new_stock)

        cursor.execute(qury,values)

        database.commit()
        print("\nSale Detail Added Successfully!")

    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error ! \n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# Update Sale Total 
#-----------------------

def update_sale_total(sale_id,cursor,database):

    qury = """
    SELECT SUM(quantity * unit_price) FROM 
    inventory_system.sale_details
    WHERE sale_id = %s
    """

    cursor.execute(qury,(sale_id,))

    result = cursor.fetchone()

    total_amount = result[0] if result[0] else 0

    qury = """
    UPDATE inventory_system.sales
    SET total_amount = %s
    WHERE sale_id = %s
    """
    cursor.execute(qury,(total_amount,sale_id))

#-----------------------
# View All Sale
#-----------------------

def view_sales():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT * FROM inventory_system.sales
        ORDER BY sale_id
        """

        cursor.execute(qury)

        sales = cursor.fetchall()

        if not sales:
            print("\nSale Not Found!")
            return
        print("\n===== All Sales =====\n")
        for sale in sales:
            print(f"""
Sale Id           : {sale[0]}
Sale Date         : {sale[1]}
Total sale Amount : {sale[2]}
------------------------------\n""")
            
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error ! \n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# Search Sale
#----------------------

def search_sale():
    
    try:
        sale_id = int(input("\nEnter Sale :"))

        if not sale_id:
            print("\nSale Id Can't be empty")
            return
    except ValueError as e:
        print("\nPlease sale id in digit\n",e)
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT  
        * FROM inventory_system.sales
        WHERE sale_id = %s
        """

        cursor.execute(qury,(sale_id,))

        sale =cursor.fetchone()

        if not sale:
            print("\nSale Not found!")
            return

        print("\n==== Sale Found ====\n")
        print(f"""
Sale Id           : {sale[0]}
Sale Date         : {sale[1]}
Total sale Amount : {sale[2]}
    ------------------------------\n""")
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error ! \n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#----------------------
# View Sale Details 
#----------------------

def view_sale_detail():
    try:
        sale_id = int(input("\nEnter Sale Id :"))
        
        if not sale_id :
            print("\nSale Id can,t be empty!")
            return
    except ValueError as e:
        print("\nSale Id must be a digit \n",e)
        return
    
    try:
        database = get_connection()
        cursor = database.cursor()
        
        qury = """
        SELECT 
        s.sale_id,
        s.sale_date,
        p.product_name,
        sd.quantity,
        sd.unit_price,
        (sd.unit_price * sd.quantity) AS Total
        FROM sales AS s JOIN sale_details AS sd
        ON s.sale_id = sd.sale_id 
        JOIN products AS p
        ON p.product_id = sd.product_id
        WHERE sd.sale_id = %s"""
        
        cursor.execute(qury,(sale_id,))
        
        sales = cursor.fetchall()
        
        if not sales:
            print("\nSale Not Found!")
            return
        
        print("\n===== Sale Details =====\n")
        
        for sale in sales:
            print(f"""
Sale Id        : {sale[0]}
Sale Date      : {sale[1]}

Product Name   : {sale[2]}
Quantity       : {sale[3]}
Unit Price     : {sale[4]}
Total          : {sale[5]}
----------------------------\n""")
        print("\nTotal Sale : ",sum(sale[5] for sale in sales))
        
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error..!\n",error)
    
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

            
#-----------------------
# Delete Sale
#-----------------------

def delete_sale():
    try:
        try:   
            database = get_connection()
            cursor = database.cursor()  

            sale_id =int(input("Enter Sale id :"))
            if not sale_id:
                print("\nSale Id can't be empty!")
                return
             
        except ValueError as e:
            print("\nId must be a number\n",e)
            return
                
        qury ="""
            SELECT sale_id FROM inventory_system.sales
            WHERE sale_id = %s
            """
        cursor.execute(qury,(sale_id,))
        sale =cursor.fetchone()
                
        if not sale:
            print("\nSale Not Exsist")
            return

        confirmation =input("\nAre You Sure to delete this Sale from database (Yes / No) :").strip().lower()

        if confirmation != "yes":
            print("\nDelete Sale Process Cancel!\n")
            return
        
        qury = """
        SELECT product_id,quantity
        FROM sale_details
        WHERE sale_id = %s
        """
        
        cursor.execute(qury,(sale_id,))
        
        detail = cursor.fetchall()
        
        for product_id,quantity in detail:
            
            # Add stock in Products 
            
            qury = """
            SELECT product_id , quantity
            FROM products
            WHERE product_id = %s"""
            
            cursor.execute(qury,(product_id,))
            
            product = cursor.fetchone()
            
            if product:
                previous_quantity = product[1]
                
                new_quantity = previous_quantity + quantity
                
                qury = """
                UPDATE products
                SET quantity = %s
                WHERE product_id = %s
                """
                
                cursor.execute(qury,(new_quantity,product_id))
                
                # Add stock History
                
                qury = """
                INSERT INTO stock_history (product_id,transcation_type,quantity,previous_quantity,new_quantity)
                VALUES (%s,%s,%s,%s,%s)
                """
                
                values = (product_id,"Stock IN",quantity,previous_quantity,new_quantity)
                
                cursor.execute(qury,values)
                
                
        qury = """
            DELETE FROM inventory_system.sales
            WHERE sale_id = %s
            """
        cursor.execute(qury,(sale_id,))

        database.commit()
        print("Sale Delete Successfully..!")
        
    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error..!\n",error)
    
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------
# Sale Menu
#-----------------------

def sale_menu():
    while True:
        print("\n======= Sale Management =======\n")

        print("1. Create Sale")
        print("2. Add Create Detail")
        print("3. View All Sales")
        print("4. Search Sale By Id")
        print("5. Delete Sale By Id")
        print("6. View Sale Detail")
        print("7. Exit ")

        try:
            choice = int(input("\nEnter Choice :"))

            if not choice :
                print("\nChoice can't be empty!")
                return
        except ValueError as e:
            print("\nPlease Enter choice in digit\n",e)

        if choice == 1:
            sale_create()
        elif choice == 2:
            sale_detail()
        elif choice == 3:
            view_sales()
        elif choice == 4:
            search_sale()
        elif choice == 5:
            delete_sale()
        elif choice == 6:
            view_sale_detail()
        elif choice == 7:
            print("\nExit From Sale Management")
            break
        else:
            print("\nInvalid Choice")
            return
