from inventory_tracking import *

Company = Firm()

## If you already have a CSV file saved.
# Company.open_csv() 

seller_juan = Sellers("Juan")
seller_beto = Sellers("Beto")
store_deposit = Stores("Deposit")
store_office = Stores("Office")
product_coffee = Products("Coffee", 150)
product_wine = Products("Wine", 120)

store_deposit.add_stock(product_coffee, 50)
store_office.add_stock(product_coffee, 25)
store_deposit.add_stock(product_wine, 70)
store_deposit.get_stock()    
move_stock(store_deposit, seller_juan, product_wine, 15)
store_deposit.get_stock()
seller_juan.get_stock()
move_stock(store_office,seller_beto ,product_coffee,200)
move_stock(store_office,seller_beto ,product_coffee,20)
store_office.get_stock()
all_stock(Company)
seller_juan.inform_sales(product_wine, 10,commission=0.05)
store_deposit.add_stock_multi((product_coffee, 25),(product_wine, 35))
all_stock(Company, valuation=True)
store_deposit.sales(product_wine, 15)
store_office.sales(product_coffee, 2, seller=seller_juan)

## To save to CSV (overwritting if it exits)
# Company.save_csv() 