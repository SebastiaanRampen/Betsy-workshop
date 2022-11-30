# Models go here

from unicodedata import name
from numpy import integer
from peewee import *


db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        database = db


# A user has a name, address data, and billing information.
# Each user must be able to own a number of products.

class User(BaseModel):
    username = CharField(primary_key = True)
    firstname = CharField()
    surname = CharField()
    address = CharField()
    billing_information = CharField()


# The products must have a name, a description, a price per unit, and a quantity describing the amount in stock.
# The price should be stored in a safe way; rounding errors should be impossible.

class Products(BaseModel):
    productname = CharField()
    description = CharField()
    seller = ForeignKeyField(User, backref = "product_to_seller")
    price = DecimalField(max_digits=2)
    stock = IntegerField()


# In order to facilitate search and categorization, a product must have a number of descriptive tags.
# The tags should not be duplicated.

class Tags(BaseModel):
    tag = CharField(primary_key = True)

class Tagged(BaseModel):
    product = ForeignKeyField(Products, backref = "tag_to_product")
    tagger = ForeignKeyField(Tags, backref = "product_to_tag")


# We want to be able to track the purchases made on the marketplace, therefore a transaction model must exist
# You can assume that only users can purchase goods
# The transaction model must link a buyer with a purchased product and a quantity of purchased items

class Transactions(BaseModel):
    buyer = ForeignKeyField(User, backref = "transaction_to_buyer")
    Product_id = ForeignKeyField(Products, backref = "transaction_of_product")
    quantity = IntegerField()



# As a bonus requirement, you must consider the various constraints for all fields and incorporate these constraints in the data model.