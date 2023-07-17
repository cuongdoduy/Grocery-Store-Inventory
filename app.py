from models import (func, Brands, session, Base, Products, engine)
import csv
import datetime

def readBrand_csv(filename):
    print("Reading Brands CSV file")
    with open(filename) as csvfile:
        data = csv.reader(csvfile)
        rows = list(data)
        for brand_row in rows[1:]:
            brand_in_db = session.query(Brands).filter(Brands.brand_name==brand_row[0]).one_or_none()
            if brand_in_db == None:
                new_brand=Brands(brand_name=brand_row[0])
                session.add(new_brand)
            session.commit()
    print("Finished reading Brands CSV file")

def readProduct_csv():
    print("Reading Products CSV file")
    with open('inventory.csv') as csvfile2:
        data = csv.reader(csvfile2)
        rows = list(data)
        for inventory_row in rows[1:]:
            product_in_db = session.query(Products).filter(Products.product_name==inventory_row[0]).one_or_none()
            if product_in_db == None:
                product_name=inventory_row[0]
                product_price=int(float(inventory_row[1][1:])*100)
                product_quantity=inventory_row[2]
                product_date_updated=datetime.datetime.strptime(inventory_row[3], '%m/%d/%Y')
                brand_id = session.query(Brands.brand_id).filter(Brands.brand_name == inventory_row[4]).scalar()
                new_product=Products(product_name=product_name,product_quantity=product_quantity,product_price=product_price,date_updated=product_date_updated,brand_id=brand_id)
                session.add(new_product)
            else:
                if (datetime.datetime.strptime(inventory_row[3], '%m/%d/%Y').date() > product_in_db.date_updated):
                    product_in_db.product_quantity=inventory_row[2]
                    product_in_db.product_price=int(float(inventory_row[1][1:])*100)
                    product_in_db.date_updated=datetime.datetime.strptime(inventory_row[3], '%m/%d/%Y')
                    brand_id = session.query(Brands.brand_id).filter(Brands.brand_name == inventory_row[4]).scalar()
                    product_in_db.brand_id=brand_id
                    session.commit()
            session.commit()
    print("Finished reading Products CSV file")

def Menu():
    print("Welcome to Mel's Inventory Application")
    print("Here are your options:")
    print("N) New Product")
    print("V) View a product by ID")
    print("A) Product Analysis")
    print("B) Backup the Database")
    print("Q) Quit the Application")
    choice=input("Enter your choice: ")
    switch(choice.upper())
def switch(choice):
    if choice=='N':
        new_product()
    elif choice=='V':
        view_product()
    elif choice=='A':
        product_analysis()
    elif choice=='B':
        backup_database()
    elif choice=='Q':
        quit_application()
    else:
        print("Invalid choice. Please try again.")
    Menu()
def new_product():
    name_product=input("What is the name of the product: ")
    try:
        quantity_product=int(input("What is the quantity of product: "))
        if quantity_product<=0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please try again.")
        quantity_product=int(input("What is the quantity of product:"))
    try:
        price_product=int(float(input("What is the price of the product: "))*100)
        if price_product<=0:
            raise ValueError
    except ValueError:
        print("Invalid input. Please try again.")
        price_product=input("What is the price of the product: ")
    try:
        date_product=input("What is the date of the product (mm/dd/yyyy): ")
        date_product=datetime.datetime.strptime(date_product, '%m/%d/%Y')
    except ValueError:
        print("Invalid input. Please try again.")
        date_product=input("What is the date of the product (mm/dd/yyyy): ")
        date_product=datetime.datetime.strptime(date_product, '%m/%d/%Y')
    brand_product=input("What is the brand of the product: ")
    brand_id = session.query(Brands.brand_id).filter(Brands.brand_name == brand_product).scalar()
    while brand_id == None:
        print("Brand not found. Please try again.")
        brand_product=input("What is the brand of the product: ")
        brand_id = session.query(Brands.brand_id).filter(Brands.brand_name == brand_product).scalar()
    product_in_db=session.query(Products).filter(Products.product_name==name_product).one_or_none()
    if product_in_db != None:
        if (date_product.date() > product_in_db.date_updated):
            product_in_db.product_quantity=quantity_product
            product_in_db.product_price=price_product
            product_in_db.date_updated=date_product
            product_in_db.brand_id=brand_id
            session.commit()
            print("Product updated.")
            print("Product ID: ", product_in_db.product_id)
            print("Product Name: ", product_in_db.product_name)
            print("Product Quantity: ", product_in_db.product_quantity)
            print("Product Price: ", product_in_db.product_price)
            print("Product Date Updated: ", product_in_db.date_updated)
            print("Product Brand: ", brand_product)
            print("--------------------")
            input("Press enter to continue")
        else:
            print("Your product is already in the database and the date is not newer than the date in the database.")
            display_product(product_in_db)
    else:
        new_product=Products(product_name=name_product,product_quantity=quantity_product,product_price=price_product,date_updated=date_product,brand_id=brand_id)
        session.add(new_product)
        session.commit()
        print("New product added.")
        print("Product ID: ", new_product.product_id)
        print("Product Name: ", new_product.product_name)
        print("Product Quantity: ", new_product.product_quantity)
        print("Product Price: ", new_product.product_price)
        print("Product Date Updated: ", new_product.date_updated)
        print("Product Brand: ", brand_product)
        print("--------------------")
        input("Press enter to continue")
    
def view_product():
    print("View a product by ID")
    product_id=input("Enter the product ID: ")
    product_in_db = session.query(Products).filter(Products.product_id==product_id).one_or_none()
    if product_in_db == None:
        print("Product not found.")
        print("Please try again.")
        print("--------------------")
        input("Press enter to continue")
        view_product()
    print("--------------------")
    print("What do you want to do?")
    print("1) Update product")
    print("2) Delete product")
    print("3) View product")
    choice=input("Enter your choice: ")
    if choice=='1':
        update_product(product_in_db)
    elif choice=='2':
        delete_product(product_in_db)
    elif choice=='3':
        display_product(product_in_db)
    else:
        print("Invalid choice. Please try again.")
        view_product()

def display_product(product_in_db: Products):
    print("Product ID: ", product_in_db.product_id)
    print("Product Name: ", product_in_db.product_name)
    print("Product Quantity: ", product_in_db.product_quantity)
    print(f"Product Price: ${product_in_db.product_price/100}")
    print("Product Date Updated: ", product_in_db.date_updated)
    brand_name=session.query(Brands.brand_name).filter(Brands.brand_id==product_in_db.brand_id).scalar()
    print("Product Brand: ", brand_name)
    print("--------------------")
    input("Press enter to continue")
    return

def update_product(product_in_db: Products):
    print("Update product")
    print("Product ID: ", product_in_db.product_id)
    print("Product Name: ", product_in_db.product_name)
    print("Product Quantity: ", product_in_db.product_quantity)
    print("Product Price: ", product_in_db.product_price)
    print("Product Date Updated: ", product_in_db.date_updated)
    brand_name=session.query(Brands.brand_name).filter(Brands.brand_id==product_in_db.brand_id).scalar()
    print("Product Brand: ", brand_name)
    print("--------------------")
    print("What do you want to update?")
    print("1) Product Name")
    print("2) Product Quantity")
    print("3) Product Price")
    print("4) Product Date Updated")
    print("5) Product Brand")
    choice=input("Enter your choice: ")
    if choice=='1':
        product_name=input("Enter the new product name: ")
        product_in_db.product_name=product_name
        session.commit()
        print("Product updated.")
        display_product(product_in_db)
    elif choice=='2':
        try:
            product_quantity=int(input("Enter the new product quantity: "))
            if product_quantity<=0:
                raise ValueError
        except ValueError:
            print("Invalid input. Please try again.")
            product_quantity=int(input("Enter the new product quantity: "))
        product_in_db.product_quantity=product_quantity
        session.commit()
        print("Product updated.")
        display_product(product_in_db)
        
    elif choice=='3':
        try:
            product_price=float(input("Enter the new product price: "))
            if product_price<=0:
                raise ValueError
        except ValueError:
            print("Invalid input. Please try again.")
            product_price=float(input("Enter the new product price: "))
        product_in_db.product_price=product_price
        session.commit()
        print("Product updated.")
        display_product(product_in_db)
    elif choice=='4':
        try:
            date_updated=datetime.datetime.strptime(input("Enter the new product date updated (YYYY-MM-DD): "),"%Y-%m-%d")
        except ValueError:
            print("Invalid input. Please try again.")
            date_updated=datetime.datetime.strptime(input("Enter the new product date updated (YYYY-MM-DD): "),"%Y-%m-%d")
        product_in_db.date_updated=date_updated
        session.commit()
        print("Product updated.")
        display_product(product_in_db)
    elif choice=='5':
        brand_name=input("Enter the new product brand: ")
        brand_in_db=session.query(Brands).filter(Brands.brand_name==brand_name).one_or_none()
        if brand_in_db==None:
            print("Brand not found.")
            print("Please try again.")
            print("--------------------")
            input("Press enter to continue")
        else:
            product_in_db.brand_id=brand_in_db.brand_id
            session.commit()
            print("Product updated.")
            display_product(product_in_db)
            input("Press enter to continue")
    else:
        print("Invalid input. Please try again.")
        print("--------------------")
        input("Press enter to continue")

def delete_product(product_in_db: Products):
    print("Do you want to delete a product?")
    print("1) Yes")
    print("2) No")
    choice=input("Enter your choice: ")
    if choice=='1':
        session.delete(product_in_db)
        session.commit()
        print("Product deleted.")
        input("Press enter to continue")
    elif choice=='2':
        pass
def product_analysis(): 
    most_expensive_product=session.query(Products.product_name).order_by(Products.product_price.desc()).first()
    print("The most expensive product is: ", most_expensive_product[0])
    least_expensive_product=session.query(Products.product_name).order_by(Products.product_price.asc()).first()
    print("The least expensive product is: ", least_expensive_product[0])
    brand_most_products=session.query(Brands.brand_name).join(Products).group_by(Brands.brand_name).order_by(func.count(Products.product_id).desc()).first()
    print("The brand with the most products is: ", brand_most_products[0])
    brand_least_products=session.query(Brands.brand_name).join(Products).group_by(Brands.brand_name).order_by(func.count(Products.product_id).asc()).first()
    print("The brand with the least products is: ", brand_least_products[0])
    average_price=session.query(func.avg(Products.product_price)).scalar()
    print("The average price of all products is: ", average_price)
    oldest_product=session.query(Products.product_name).order_by(Products.date_updated.asc()).first()
    print("The oldest product is: ", oldest_product[0])
    newest_product=session.query(Products.product_name).order_by(Products.date_updated.desc()).first()
    print("The newest product is: ", newest_product[0])
    print("--------------------")
    input("Press enter to continue")

def backup_database():
    print("Backing up the database")
    with open('backup_inventory.csv', 'w') as csvfile:
        fieldnames = ['product_name', 'product_quantity', 'product_price', 'date_updated', 'brand_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        products=session.query(Products).all()
        for product in products:
            brand_name=session.query(Brands.brand_name).filter(Brands.brand_id==product.brand_id).scalar()
            writer.writerow({'product_name': product.product_name, 'product_quantity': product.product_quantity, 'product_price': f"${product.product_price/100}", 'date_updated': product.date_updated.strftime("%m/%d/%Y"), 'brand_name': brand_name})
    with open('backup_brands.csv', 'w') as csvfile:
        fieldnames = ['brand_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        brands=session.query(Brands).all()
        for brand in brands:
            writer.writerow({'brand_name': brand.brand_name})
    print("Finished backing up the database")
    print("--------------------")
    input("Press enter to continue")

def quit_application():
    print("Thank you for using Mel's Inventory Application")
    exit()

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    readBrand_csv('brands.csv')
    readProduct_csv()
    Menu()
