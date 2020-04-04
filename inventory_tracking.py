import pandas as pd
from collections import defaultdict
from datetime import datetime

class Products:
    
    def __init__(self, name, price=0):
        self.name = name
        self.price = price

    def __repr__(self):
        return "Product: {}".format(self.name)

    def get_price(self):
        """ Get current price assigned to the product.
        """

        return self.price
    
    def set_price(self, price):
        """ Assign a new price to the product.
        """ 
        
        self.price = price
        return self.price


class Firm():
    full_list = list()
    transactions_record = pd.DataFrame(columns=['Date','Origin','Destinatary','Product','Quantity','Total Amount','Commission','Add Stock','Sell'])

  
    def __init__(self, name=None):
        self.ProductsDict = defaultdict(int)
        self.name = name

    def add_stock(self, product, quantity):
        """ Add stock for a specific product. 
        Can be use either for Sellers or Stores objects.

        Parameters
        ---------
        product: object
        quantity: int
        """

        self.ProductsDict[product] += int(quantity)
        add_remove = "Added" if quantity > 0 else "Removed"
        print("{} {} u. of {}".format(add_remove, quantity, product.name))
        ## DataFrame appending ##
        dictio = {'Date': datetime.today(), 'Destinatary': self.name, 'Product': product.name, 'Quantity': quantity, 'Add Stock': True}
        Firm.transactions_record = Firm.transactions_record.append(dictio, ignore_index=True)

    def add_stock_multi(self, *arg):
        """ Add stock for one or multiple  products. 
        Can be use either for Sellers or Stores objects.
        
        Parameters
        ---------
        product: object
        quantity: int

        This should be passed as: (product, quantity)
        """

        for pair in arg:
            product = pair[0]
            quantity = pair[1]
            self.ProductsDict[product] += int(quantity)
            add_remove = "Added" if quantity > 0 else "Removed"
            print("{} {} u. of {}".format(add_remove, quantity, product.name))
            ## DataFrame appending ##
            dictio = {'Date': datetime.today(), 'Destinatary': self.name, 'Product': product.name, 'Quantity': quantity, 'Add Stock': True}
            Firm.transactions_record = Firm.transactions_record.append(dictio, ignore_index=True)

    def get_stock(self):
        """ Get an inventory list of products with it's quantities for an specific Seller or Store object.
        """
        
        print("{0}: Current Stock".format(self.name))
        for k,v in self.ProductsDict.items():
            print("{0} = {1} u.".format(k.name, v))
    
    def current_stock_valuation(self):
        """ Get an inventory list of products with it's quantities and total valuation for an specific Seller or Store object.
        If it's called on a Seller, it will also calculate the potential commission for selling all the inventory.
        """

        print("{0}: Current Stock Valuation".format(self.name))
        total_acum = 0
        com_acum = 0
        for product,quantity in self.ProductsDict.items():
            total_prod = product.price*quantity
            total_acum += total_prod
            print("{0} x {1} u. = $ {2}".format(product.name, quantity,total_prod))
            if isinstance(self, Sellers):
                com = product.price*self.commission
                com_acum += com
        print("Total stock valuation: $ {}".format(total_acum))  
        if isinstance(self, Sellers):
            print("Potential comission: $ {}".format(com_acum)) 
    
    def open_csv(self, filename='transactions_record.csv'):
        """ Open a csv file with records of transactions previosly stored.
        CAUTION: it will overwrite the current DataFrame assigned to the Firm.
        """

        Firm.transactions_record = pd.read_csv(filename, sep=';',index_col=0)
        print("CSV file '{}' loaded".format(filename))
        
    def save_csv(self, filename='transactions_record.csv'):
        """ Save the current DataFrame of records to a csv file.
        CAUTION: if there is a file with the same name, it will be overwritten.
        """

        Firm.transactions_record.to_csv(str(filename), index=True, sep=';', date_format='%Y-%m-%d')


class Sellers(Firm):

    def __init__(self, name=None, commission=0.02):
        super().__init__(self)
        self.name = name
        self.commission = float(commission)
        super().full_list.append(self)

    def __repr__(self):
        return "Seller: {}".format(self.name)

    def get_commission(self):
        """ Get current commission assigned to the Seller.
        """

        return self.commission
    
    def set_commision(self, commission):
        """ Assign a commission percentage to the Seller.
        Should be set as decimal number (e.g. 0.05)
        """
        self.commission = float(commission)

    def inform_sales(self, product, quantity, commission=None, price=None, total=None):
        """ Inform the sales done by a Seller. 
        Calculates the corresponding commission those sales.

        Parameters:
        ----------
        product: object
        quantity: int
        commission: float (optional)
        price: int (optional)
        total: int (optional)

        The commission, price (of each product) and total (of the sales) are optional.
        If they are not provided they are calculated with the stored values of price (Product) and commission (Seller).
        """

        com = commission if commission else self.commission
        price_u = price if price else product.price
        total_sold = total if total else quantity*price_u
        self.ProductsDict[product] -= int(quantity)       
        seller_com = total_sold*com
        print("Total sold by {} : $ {:.2f}. Commission: $ {:.2f}".format(self.name, total_sold, seller_com))
        ## DataFrame appending ##
        dictio = {'Date': datetime.today(), 'Origin': self.name, 'Product': product.name, 'Quantity': quantity, 'Total Amount': total_sold, 'Commission':seller_com, 'Sell': True}
        Firm.transactions_record = Firm.transactions_record.append(dictio, ignore_index=True)


class Stores(Firm):

    def __init__(self, name=None):
        super().__init__(self)
        self.name = name
        super().full_list.append(self)

    def __repr__(self):
        return "Store: {}".format(self.name)

    def sales(self, product=None, quantity=None, price=None, commission=None, total=None, seller=None):
        """ Perform sales directly from the Stores.
        If a Seller is assigned. It will first move the stock from the Store to the Seller, and then perform the sale.

        Parameters:
        ----------
        product: object
        quantity: int
        price: int (optional)
        commission: float (optional)
        total: int (optional)
        seller: object (optional)

        The price (of each product) and total (of the sales) are optional. 
        If they are not provided they are calculated with the stored values of price.
        In the case you assign a seller to perfom the sales, you can assign a custom commission as well.
        """

        if seller is not None:
            move_stock(origin=self, receiver=seller, product=product, quantity=quantity)
            return seller.inform_sales(product, quantity, price, commission, total)
        else:
            price_u = price if price else product.price
            total_sold = total if total else quantity*price_u
            self.ProductsDict[product] -= int(quantity)
            print("Total sold from {} : $ {:.2f}.".format(self.name, total_sold))
            ## DataFrame appending ##
            dictio = {'Date': datetime.today(), 'Origin': self.name, 'Product': product.name, 'Quantity': quantity, 'Total Amount': total_sold, 'Sell': True}
            Firm.transactions_record = Firm.transactions_record.append(dictio, ignore_index=True)       


## General Functions ##
def move_stock(origin, receiver, product, quantity=1):
    """ Move stock from one Seller or Store to another.
    No sales involved.
    """

    if origin.ProductsDict[product]-quantity >= 0:
        origin.ProductsDict[product] -= quantity
        receiver.ProductsDict[product] += quantity
        print("Succesfully moved {} u. of {} from {} to {}".format(quantity, product.name, origin.name, receiver.name))
        ## DataFrame appending ##
        dictio = {'Date': datetime.today(), 'Origin': origin.name, 'Destinatary': receiver.name, 'Product': product.name, 'Quantity': quantity}
        Firm.transactions_record = Firm.transactions_record.append(dictio, ignore_index=True)
    else:
        print("There are only {} u. avaiable of {}".format(origin.ProductsDict[product], product.name))

def all_stock(cls, valuation=False):
    """ Return a list of the inventory.
    Optionaly, it could show the valuation of the inventory.

    Parameter:
    valuation: boolean (default:False)
    """

    print("_Segregated Stock_")
    ProductsDictFull = defaultdict(int)
    valuation_total = 0
    for holder in cls.full_list:
        valuation_each = 0
        for product, quantity in holder.ProductsDict.items():
            ProductsDictFull[product] += quantity
            print("{:12.10} --> {:12.10} : {} u.".format(holder.name, product.name, quantity))
            if valuation:
                valuation_each += product.price*quantity
        if valuation:
            print("Stock valuation: $ {}".format(valuation_each))
            valuation_total += valuation_each
    print(" ")
    print("_Acumulated Stock_")
    for product, quantity in ProductsDictFull.items():
        print("{:12.10} : {} u.".format(product.name, quantity))
    if valuation:
        print("Stock valuation: $ {}".format(valuation_total))

## DataFrame Functions ##
def last_movements(quantity=5):
    return Firm.transactions_record.tail(quantity)

def total_sales():
    df = Firm.transactions_record
    df_filtered = df[df['Sell'] == True ]
    return df_filtered.groupby('Origin')['Total Amount','Commission'].sum()

def all_movements(seller_store):
    df = Firm.transactions_record
    return df[(df['Origin'] == seller_store) | (df['Destinatary'] == seller_store)]

def sales_by_seller(seller):
    df = Firm.transactions_record
    df_filtered = df[df['Sell'] == True ]
    return df_filtered[df_filtered['Origin'] == seller]

def sales_by_product(product):
    df = Firm.transactions_record
    df_filtered = df[df['Sell'] == True ]
    return df_filtered[df_filtered['Product'] == product]



