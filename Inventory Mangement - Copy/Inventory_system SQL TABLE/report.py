from database import get_connection
import mysql.connector
from stock import view_stock_history
#-------------------
# sale reports
#-------------------

def view_sale_report():
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
        ORDER BY sale_id"""
        
        cursor.execute(qury)
        
        sales = cursor.fetchall()
        
        if not sales:
            print("\nSale Not Found!")
            return
        
        print("\n===== Sale Details Reports =====\n")
        
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

#------------------------
# View Purchase REport
#------------------------

def view_purchase_report():
    try:
        database = get_connection()
        cursor = database.cursor()

        qury = """
        SELECT 
            p.purchase_id,
            p.purchase_date,
            s.supplier_name,
            po.product_name,
            pd.quantity,
            pd.unit_price,
            (pd.quantity * pd.unit_price) AS Total
            
        FROM inventory_system.suppliers as s 
        JOIN
        inventory_system.purchases as p
        ON 
        s.supplier_id = p.supplier_id
        JOIN 
        inventory_system.purchase_details as pd
        ON
        p.purchase_id = pd.purchase_id 
        JOIN
        inventory_system.products as po
        ON
        pd.product_id = po.product_id
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
    Purchase Date     : {purchase[1]}
    
    Supplier Name     : {purchase[2]}
    Product Name      : {purchase[3]}
    Quantity          : {purchase[4]}
    Unit Price        : {purchase[5]}
    Total Amount      : {purchase[6]}
    -----------------------------\n""") 
    except mysql.connector.Error as error:
        print("\nDatabase Error !\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#---------------------
# Current Stock Reports
#---------------------

def view_stock_reports():
    try:
        database = get_connection()
        cursor = database.cursor()
        
        qury = """
        SELECT 
        p.product_id ,
        p.product_name,
        s.supplier_name,
        p.category,
        p.price,
        p.quantity
        FROM products as p 
        JOIN suppliers as s
        ON p.supplier_id = s.supplier_id
        ORDER BY product_id
        """
        
        cursor.execute(qury)
        
        products = cursor.fetchall()
        
        if not products:
            print("\nStock Report not Found!")
            return
        
        print("\n==== Stock Report ====\n")
        for product in products:
            print(f"""
    Product Id      : {product[0]}
    Product Name    : {product[1]}
    Supplier Name   : {product[2]}
    Category        : {product[3]}
    Price           : {product[4]}
    Quantity        : {product[5]}
    -------------------------------\n""")
            
    except mysql.connector.Error as error:
        print("\nDatabase Error!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#--------------------
#Sale Summary Report
#------------------

def sale_summary_report():
    try:
        database = get_connection()
        cursor = database.cursor()
        
        qury = """
        SELECT COUNT(DISTINCT s.sale_id),
        COALESCE (SUM(sd.quantity),0) ,
        COALESCE (SUM(sd.quantity * sd.unit_price),0) 
        FROM sales as s 
        JOIN sale_details as sd ON
        s.sale_id = sd.sale_id
        """
        
        cursor.execute(qury)
        
        result = cursor.fetchone()
        
        print("\n==== Sale Summary ====\n")
        
        print(f"Total Sales             : {result[0]}")
        print(f"Total Item Sold         : {result[1]}")
        print(f"Total Sale Amount       : {result[2]}")
        try:
            choice = input("\nAre You want to check Sale Report(Yes or No):").strip().lower()
            
            if  choice == "yes" :
                view_sale_report()
            elif choice == "no":
                return
            else:
                print("\nPlease Enter YES or NO")
                return
        except :
            print("\nInvalid Choice")
        
    except mysql.connector.Error as error:
        print("\nDatabase Error!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#---------------------
# Purchase Summary Reports 
#--------------------
def purchase_summary_report():
    try:
        database = get_connection()
        cursor = database.cursor()
        
        qury = """
        SELECT COUNT(DISTINCT p.purchase_id ),
        COALESCE(SUM(pd.quantity),0),
        COALESCE(SUM(pd.quantity * pd.unit_price),0)
        FROM purchases AS p
        JOIN 
        purchase_details AS pd
        ON
        p.purchase_id = pd.purchase_id
        """
        
        cursor.execute(qury)
        
        result = cursor.fetchone()
        
        print("\n==== Purchase Summary ====\n")
        
        print(f"Total Purchase              : {result[0]}")
        print(f"Total Item Buy              : {result[1]}")
        print(f"Total Purchase Amount       : {result[2]}")
        try:
            choice = input("\nAre You want to check Purchase Report(Yes or No):").strip().lower()
            
            if  choice == "yes" :
                view_purchase_report()
            elif choice == "no":
                return
            else:
                print("\nPlease Enter YES or NO")
                return
        except :
            print("\nInvalid Choice")
        
    except mysql.connector.Error as error:
        print("\nDatabase Error!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#----------------------
# Stock Summary Report
#---------------------

def stock_summary_report():
    try:
        database = get_connection()
        cursor = database.cursor()
        
        qury = """
        SELECT COUNT(product_id ),
        COALESCE(SUM(quantity),0),
        COALESCE(SUM(quantity * price),0)
        FROM products
        """
        
        cursor.execute(qury)
        
        result = cursor.fetchone()
        
        print("\n==== Stock Summary ====\n")
        
        print(f"Total Product              : {result[0]}")
        print(f"Total Stock                : {result[1]}")
        print(f"Total stock Amount         : {result[2]}")
        try:
            choice = input("\nAre You want to check Stock Report(Yes or No):").strip().lower()
            
            if  choice == "yes" :
                view_stock_reports()
            elif choice == "no":
                return
            else:
                print("\nPlease Enter YES or NO")
                return
        except :
            print("\nInvalid Choice")
        
    except mysql.connector.Error as error:
        print("\nDatabase Error!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()

#------------------------
# Profit Or Lose Base on Whole Purchase and Sale 
#------------------------

def profit_lose_report():
    try:
        database = get_connection()
        cursor = database.cursor()
        
        sale_qury = """
        SELECT COALESCE(SUM(total_amount),0)
        FROM sales"""
        
        purchase_qury = """
        SELECT COALESCE(SUM(total_amount),0)
        FROM purchases"""
        
        cursor.execute(sale_qury)
        total_sale = cursor.fetchone()[0]
        
        cursor.execute(purchase_qury)
        total_purchase =cursor.fetchone()[0]
        
        profit_lose = total_sale - total_purchase
        
        print("\n==== Profit / Lose Summary ====\n")
        
        print(f"Total Purchase Amount :{total_purchase}")
        print(f"Total Sale Amount     :{total_sale}")
        print(f"Profit / Lose         :{profit_lose}")
        
        if profit_lose > 0:
            print("\nStatus           : Profit")
        elif profit_lose < 0:
            print("\nStatus           : Lose")
        else:
            print("\nStatus           : No Lose / No Profit")
            
    except mysql.connector.Error as error:
        print("\nDatabase Error!\n",error)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "database" in locals() and database.is_connected():
            database.close()
                
        
#----------------------
# Report Menu
#---------------------

def report_menu():
    while True:
        print("\n**** Reports Menu ****\n")
        
        print("1. Sale Reports")
        print("2. Purchase Reports")
        print("3. Stock Reports")
        print("4. Stock Transfer Reports")
        print("5. Sale Summary Report")
        print("6. Purchase Summary Report")
        print("7. Stock Summary Report")
        print("8. Profit / Lose Summary")
        print("9. Back")
        
        try:
            choice = int(input("\nEnter The Choice :"))
            
            if not choice:
                print("\nChoice Can't be empty!")
                return
        except ValueError as e:
            print("\nPlease Enter choice in number \n",e)
            return
        
        if choice == 1:
            view_sale_report()
        elif choice == 2:
            view_purchase_report()
        elif choice == 3:
            view_stock_reports()
        elif choice == 4:
            view_stock_history()
        elif choice == 5:
            sale_summary_report()
        elif choice == 6:
            purchase_summary_report()
        elif choice == 7:
            stock_summary_report()
        elif choice == 8:
            profit_lose_report()
        elif choice == 9:
            print("\nBack to main Menu")
            return
        else:
            print("\nInvalid Choice!")
            return