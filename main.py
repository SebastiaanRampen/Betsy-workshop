__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import os
from models import *
from peewee import *

from setup_db import populate_test_data



def search(term):
    return Products.select(Products.productname).where(Products.description.contains(term) | 
    Products.productname.contains(term))



def list_user_products(user_id):
    # return User.select(Products.productname).where(
    #     User.username == user_id).join(
    #      Products, JOIN.INNER
    # )
    results = User.select(Products.productname).where(
        User.username == user_id).join(
         Products, JOIN.INNER
    )
    specific_results = []
    for x in results:
        specific_results.append(x.products.productname)
    return specific_results


def list_products_per_tag(tag_id):
    return Tagged.select(Products.productname).where(
        Tagged.tagger == tag_id).join(Products, JOIN.INNER)


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

    # results = search('AA')
    # for result in results:
    #     print (result.productname)

    # results = list_user_products('MandyMoes')
    # for result in results:
    #     # print (result.products.productname)
    #     print (result)


    # results = list_products_per_tag('fruit')
    # for result in results:
    #     print (result.product.productname)

    # add_product_to_catalog("Rabarber", "Bijgerecht van rabarber", "VeRAbarber", 4.00, 60,["zoet", "lekkernij", "bijgerecht", "taart"])
    # add_taggs_to_product("Rabarber", "VeRAbarber", ["heerlijk"])    

    # update_stock(7, 3)
    # purchase_product(7, "PeterPeer", 5)

    # remove_product(7)


    print("closing")
    # db.close()


if __name__ == "__main__":
    main()
