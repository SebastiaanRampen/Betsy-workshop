from models import (
    db,
    User,
    Products,
    Tags,
    Tagged,
    Transactions,
    )
import os


def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)


def populate_test_data():
    db.connect()

    db.create_tables(
        [
            User,
            Products,
            Tags,
            Tagged,
            Transactions,
        ]
    )

    user_input = {
            "MandyMoes" : [
                "Mandy",
                "Moes",
                "Moestuin 3",
                "NL10BANK01325476"
            ],
            "PeterPeer" : [
                "Peter",
                "Peer",
                "Perenboom 8a",
                "NL20BANK02143657"
            ],
            "VeRAbarber" : [
                "Vera",
                "Rabarber",
                "Ooievaarsbek 9",
                "NL23BANK03142756"
            ],
            "Chutney" : [
                "Churandy",
                "De Boer",
                "Pepermolen 112",
                "NL03BANK01526374"
            ],

    }
    for new_user, user_data in user_input.items():
        User.create(
            username = new_user,
            firstname = user_data[0],
            surname = user_data[1],
            address = user_data[2],
            billing_information = user_data[3],
        )


    product_input = {
        "Aardbeienjam" : [
            "Jam, gemaakt van aardbeien",
            "MandyMoes",
            2.59,
            20,
        ],
        "Sperzieboontjes" : [
            "Voorgekookte sperzieboontjes",
            "PeterPeer",
            0.79,
            50,
        ],
        "Rote Grütze" : [
            "Desert, gemaakt van rode vruchten",
            "VeRAbarber",
            3.25,
            15,
        ],
        "Piccalilly" : [
            "Groentenmengsel, ingelegd in zuur",
            "Chutney",
            3.30,
            40,
        ],
        "Stoofpeertjes" : [
            "Gestoofte peertjes",
            "PeterPeer",
            2.99,
            15,
        ],
        "Boerenjongens" : [
            "Rozijnen op brandewijn",
            "MandyMoes",
            3.99,
            20,
        ],
        "Boerenmeisjes" : [
            "Abrikozen op brandewijn",
            "MandyMoes",
            3.99,
            20,
        ],
    }
    for new_product, product_data in product_input.items():
        Products.create(
            productname = new_product,
            description = product_data[0],
            seller = product_data[1],
            price = float(product_data[2]),
            stock = int(product_data[3]),
        )
    
    new_tags = ["fruit", "groente", "vers", "ingevroren",
        "zuur", "zoet", "zout", "alcohol", "hoofdgerecht",
        "nagerecht", "bijgerecht", "lekkernij", "broodbeleg"]
    for tag_data in new_tags:
        Tags.create(tag = tag_data)



    tag_links = {
        1: [1, "fruit"],
        2: [1 , "broodbeleg"],
        3: [1 , "zoet"],
        4: [7 , "lekkernij"],
        5: [7 , "fruit"],
        6: [7 , "alcohol"],
        7: [6 , "lekkernij"],
        8: [6 , "fruit"],
        9: [6 , "alcohol"],
        10: [4 , "groente"],
        11: [4 , "zuur"],
        12: [4 , "bijgerecht"],
        13: [5 , "fruit"],
        14: [5 , "zoet"],
        15: [5 , "hoofdgerecht"],
        16: [5 , "lekkernij"],
        17: [2 , "groente"],
        18: [2 , "hoofdgerecht"],
        19: [2 , "ingevroren"],
        20: [3 , "fruit"],
        21: [3 , "ingevroren"],
        22: [3 , "zoet"],
        23: [3 , "nagerecht"],
        24: [3 , "lekkernij"],
    }

    for id_nr, tag_info in tag_links.items():
        Tagged.create(product = tag_info[0], tagger = tag_info[1])


    previous_transactions = {
        "VeRAbarber" : [4, 4], 
        "MandyMoes" : [2, 5],
        "Chutney" : [1, 8],
    }
    for add_transactions, transaction_data in previous_transactions.items():
        Transactions.create(
            buyer = add_transactions, 
            Product_id = transaction_data[0],
            quantity = transaction_data[1])

    db.close()