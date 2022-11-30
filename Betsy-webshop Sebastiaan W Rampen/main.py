__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import os
from models import *
from peewee import *

from setup_db import populate_test_data

def search(term):
    products_found = False    
    for one_product in Products.select().dicts():
        if one_product["productname"].lower().find(term.lower()) > -1 or\
            one_product["description"].lower().find(term.lower()) > -1 :
            if products_found == False:
                products_found = True
                print(f'All products with "{term}" in the productname or description:')
            print(one_product["productname"])
    if products_found == False:
        print(f'No products found with "{term}" in the productname or description')


def list_user_products(user_id):
    product_list = User.select(Products.productname).where(
        User.username == user_id).join(
         Products, JOIN.INNER
    )
    if len(product_list) > 0:
        print("All products for user:", user_id)
        for individual_product in product_list:
            print(individual_product.products.productname)    
    else: print("No products found for user:", user_id)


def list_products_per_tag(tag_id):
    tagged_list = Tagged.select(Products.productname).dicts().where(
        Tagged.tagger == tag_id).join(Products, JOIN.INNER)
    if len(tagged_list) > 0:    
        print(f'All products with the tag "{tag_id}"')
        for item in tagged_list:
            print(item["productname"])
    else: print(f'No products with the tag "{tag_id}"')    


def add_tag_to_table(add_tag):
    query = Tags.get_or_none(Tags.tag == add_tag)
    if query is None:
        Tags.create(tag = add_tag)


def add_taggs_to_product(product, user_id, add_tags):
    print(f'Add tags to the product "{product}" from "{user_id}"')

    product_to_add = Products.get_or_none(Products.productname == product, Products.seller == user_id)
    if product_to_add is None:
        print(product, "sold by", user_id, "is not yet available")
    else:
        print(product_to_add)
        for add_tag in add_tags:
            add_tag_to_table(add_tag)
            Tagged.create(product = product_to_add, tagger = add_tag)



def add_product_to_catalog(product, description, user_id, price, nr_of_items, product_tags):
    product_present = User.select(Products.productname).where(
        User.username == user_id).where(Products.productname==product).join(
         Products, JOIN.INNER
    )
    if len(product_present) > 0:
        print(f'{product} is already present in the catalog of {user_id}')
    else:
        print(f'Adding the product "{product}" from "{user_id}" to the catalog')
        new_product = Products.create(
            productname = product,
            description = description,
            seller = user_id,
            price = price,
            stock = nr_of_items,
            ).productname
        add_taggs_to_product(new_product, user_id, product_tags)


def update_stock(product_id, new_quantity):
    active_product = Products.get_or_none(Products.id == product_id)
    if active_product == None:
        print(f'No product found with product id: {product_id}')
    else:    
        print(f'Stock of {active_product.productname} before: {active_product.stock}')
        active_product.stock += new_quantity
        active_product.save()
        print(f'Stock of {active_product.productname} after: {active_product.stock}')


def purchase_product(product_id, buyer_id, quantity_bought):
    active_product = Products.get_or_none(Products.id == product_id)
    if active_product == None:
        print(f'No product found with product id: {product_id}')
    else:
        if active_product.stock < quantity_bought:
            print(f'Not enough items availabe. Only {active_product.stock} in stock')
        else:
            active_buyer = User.get_or_none(User.username == buyer_id)
            if active_buyer == None:
                print(f'No user found with the user id {buyer_id}')
            else:    
                print(f'{active_buyer} buys {quantity_bought} items of {active_product.productname}')
                Transactions.create(buyer = active_buyer,
                    Product_id = active_product,
                    quantity = quantity_bought)
                active_product.stock -= quantity_bought
                active_product.save()
                if active_product.stock == 0:
                    print(f'No more items of {active_product.productname} available')


def remove_product(product_id):
    active_product = Products.get_or_none(Products.id == product_id)
    if active_product == None:
        print(f'No products available with product id {product_id}')
    else:
        print(f'The product {active_product.productname} has been removed from the database')

        query = Tagged.delete().where(Tagged.product == active_product)
        query.execute()

        query = Products.delete().where(Products.id == product_id)
        query.execute()
 

def main():
    # db.connect()
    # als de database gevuld moet worden, dan zit de 
    # db.connect() en db.close() in dit gedeelte in de weg
    # omdat de db dan te vroeg wordt afgesloten
    # Verder lijkt het, voor de andere 'commando's' niet nodig
    # Hoe kan dat?


    print("start")

    if not os.path.exists('database.db'):
        populate_test_data()

    # search('wijn')
    # list_user_products('MandyMoes')
    # list_products_per_tag('fruit')
    # list_products_per_tag('fruim')

    # add_product_to_catalog("Rabarber", "Bijgerecht van rabarber", "VeRAbarber", 4.00, 60,["zoet", "lekkernij", "bijgerecht", "taart"])
    # add_taggs_to_product("Rabarber", "VeRAbarber", ["heerlijk"])    

    # update_stock(7, 3)
    # purchase_product(7, "PeterPeer", 5)

    # remove_product(7)


    print("closing")
    # db.close()


if __name__ == "__main__":
    main()
