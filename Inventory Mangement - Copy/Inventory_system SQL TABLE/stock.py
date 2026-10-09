from database import get_connection
import mysql.connector

def view_stock():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury ="""
        SELECT *FROM inventory_system.products
        ORDER BY product_id
        """

        cursor.execute(qury)

        stocks = cursor.fetchall()

        if not stocks:
            print("\nProduct Not found")
            return

        print("\n======== CURRENT STOCK =========\n")

        for stock in stocks:
            print(f"""
    Product Id    : {stock[0]}
    Product Name  : {stock[1]}
    Category      : {stock[2]}
    Price         : {stock[3]}
    Quantity      : {stock[4]}
    Supplier Id   : {stock[5]}
    -----------------------------\n""")
    except mysql.connector.Error as error:
        print("\nDatabase Error\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
# Increase Stock 
#-----------------------

def increase_stock():
    try:
        product_id = int(input("\nEnter Product Id :"))

        if not product_id:
            print("\nProduct Id cannot be empty!")
            return
        quantity = int(input("Enter Quantity to Add :"))
    except ValueError as e :
        print("\nPlease enter valid number\n",e)
        return

    if quantity <= 0:
        print("\nQuantity must be greater than zero")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT product_id ,quantity FROM inventory_system.products
        WHERE product_id = %s
        """

        cursor.execute(qury,(product_id,))

        product = cursor.fetchone()

        if not product:
            print("\nProduct Id not Found!")
            return
        
        previous_stock = product[1]
        new_stock = previous_stock + quantity


        qury = """
        UPDATE inventory_system.products
        SET quantity = quantity + %s
        WHERE product_id = %s
        """

        cursor.execute(qury,(quantity,product_id))

        qury = """
        INSERT INTO inventory_system.stock_history
        (product_id,transcation_type,quantity,previous_quantity,new_quantity)
        VALUES (%s,%s,%s,%s,%s)
        """
        values = (product_id,"Stock IN",quantity,previous_stock,new_stock)

        cursor.execute(qury,values)

        database.commit()


        print("\nQuantity Add successfully In Inventory")
        print("Current Stock : ",new_stock,"\n")

    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error !\n",error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------
# Remove 
#-----------------------

def remove_stock():
    try:
        product_id = int(input("\nEnter Product Id :"))

        if not product_id:
            print("\nProduct Id cannot be empty!")
            return
        quantity = int(input("Enter Quantity to Out :"))
    except ValueError as e :
        print("\nPlease enter valid number\n",e)
        return

    if quantity <= 0:
        print("\nQuantity must be greater than zero")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT product_id,product_name,quantity
        FROM inventory_system.products
        WHERE product_id = %s
        """

        cursor.execute(qury,(product_id,))

        product = cursor.fetchone()

        if not product:
            print("\nProduct Not Found!")
            return

        previous_stock = product[2]

        if quantity > previous_stock:
            print("\nInsufficient Stock!")
            print(f"Current Stock : {previous_stock}")
            return

        new_stock = previous_stock - quantity

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
        values = (product_id,"Stock OUT",quantity,previous_stock,new_stock)

        cursor.execute(qury,values)

        database.commit()
        

        print("\nStock Out Successfully!")
        print("current Stock : ",new_stock,"\n")

    except mysql.connector.Error as error:
        database.rollback()
        print("\nDatabase Error !\n",error)

    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#-----------------------
#Search Stock by name
#----------------------
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


#-----------------------
# View Stock History 
#----------------------

def view_stock_history():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT s.stock_history_id,
        p.product_name,
        s.transcation_type,
        s.quantity,
        s.previous_quantity,
        s.new_quantity,
        s.trascation_date
        FROM inventory_system.stock_history as s
        JOIN inventory_system.products as p
        ON s.product_id = p.product_id
        ORDER BY stock_history_id
        """

        cursor.execute(qury)

        transcations = cursor.fetchall()

        if not transcations:
            print("\nStock Transfer Not Found !")
            return

        print("\n======= Stock Transfer History =======\n")
        for transcation in transcations :
            print(f"""
Transfer Id       : {transcation[0]}
Product Name      : {transcation[1]}
Transcation Type  : {transcation[2]}
Transfer Quantity : {transcation[3]}
Previous Quantity : {transcation[4]}
Current Quantity  : {transcation[5]}
Transfer Date     : {transcation[6]}
-------------------------------------\n""")
    except mysql.connector.Error as error:
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------
# Stock Search By Name 
#----------------------

def search_stock_history():
    product_name = input("\nEnter Product Name :").strip().capitalize()

    if not product_name:
        print("\nProduct Name can't be empty!")
        return
    if product_name.isdigit():
        print("\nProduct Name cannot be contain only digit")
        return
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT s.stock_history_id,
        p.product_name,
        s.transcation_type,
        s.quantity,
        s.previous_quantity,
        s.new_quantity,
        s.trascation_date
        FROM inventory_system.stock_history as s
        JOIN inventory_system.products as p
        ON s.product_id = p.product_id
        where product_name = %s
        """

        cursor.execute(qury,(product_name,))

        transcations = cursor.fetchall()

        if not transcations:
            print("\nStock Transfer Not Found !")
            return

        print("\n======= Stock Transfer History =======\n")
        for transcation in transcations :
            print(f"""
Transfer Id       : {transcation[0]}
Product Name      : {transcation[1]}
Transcation Type  : {transcation[2]}
Transfer Quantity : {transcation[3]}
Previous Quantity : {transcation[4]}
Current Quantity  : {transcation[5]}
Transfer Date     : {transcation[6]}
-------------------------------------\n""")
    except mysql.connector.Error as error:
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------
# Stock Menu
#------------------------

def stock_menu():
    while True:
        print("\n*** Stock Management ***\n")

        print("1. View Stock In Inventory")
        print("2. Add Stock In Inventory")
        print("3. Out Stock From Inventory")
        print("4. Search Stock By Name")
        print("5. View Stock Transfer")
        print("6. Search Stock Transfer By Name")
        print("7. Exit")

        try:
            choice = int(input("\nEnter Choice :"))

            if not choice:
                print("\nChoice can't be empty!")
                return
        except ValueError as e:
            print("\nChoice must be a number\n",e)

        if choice == 1:
            view_stock()
        elif choice == 2:
            increase_stock()
        elif choice == 3:
            remove_stock()
        elif choice == 4:
            search_product()
        elif choice == 5:
            view_stock_history()
        elif choice == 6:
            search_stock_history()
        elif choice == 7:
            print("\nExit From Stock Management\n")
            break
        else:
            print("\nInvalid Choice")
            return
