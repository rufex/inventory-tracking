# Inventory tracking

> Script for tracking the inventory of a small firm, between stores/deposits and sellers.

## Description

 Create a Firm with Stores/Deposits, Sellers and different Products. Assign and transfer the stock of each product between the Stores and the Sellers. Keep track of your inventory and every change to it. Register the sales done. Export the list of all the transactions to a csv file.

## How to use it

You will need to create a Firm object:

```python
Company = Firm()
```

You will need to create the objects for the Stores, Sellers and Products.

```python
seller_obj = Sellers("Seller Name")
store_obj = Stores("Store Name")
product_obj = Products("Product Name", price_sale)
```

And then you are ready to start using it (If you have used it before, you should load the csv previosuly stored).
In the `example.py` file there are some common use cases to get familiar with it's functionality.

## Comments

The goal of this side-project was to create a mockup of a simple inventory tracking sofware that I needed to use. It could be used like this (probably with some minor adjustments for practicity), but the idea is to use it in the future as the starting point for a project that includes a database and a user-friendly interface.
