import os
import sqlite3
from xml.etree import ElementTree as ET


def save_database():
    conn = sqlite3.connect('octgn.db')
    print("Database created")

    conn.execute('''DROP TABLE CARDS;''')
    print("Table dropped")

    conn.execute('''
    CREATE TABLE CARDS(
         ID             TEXT PRIMARY KEY        NOT NULL,
         CARD_ID        TEXT                    NOT NULL,
         CARD_NAME      TEXT                    NOT NULL,
         CARD_NUMBER    TEXT                     NOT NULL,
         SET_NAME       TEXT                    NOT NULL,
         SET_SHORT_NAME TEXT                    NOT NULL);
         ''')
    print("Table created")

    set_list = []
    for root, dirs, files in os.walk(
            "E:/Games/Octgn/Data/GameDatabase/A6C8D2E8-7CD8-11DD-8F94-E62B56D89593"):
        for file in files:
            if file.endswith(".xml"):
                set_list.append(os.path.join(root, file))
    sets = {}
    index = 0
    for set_file in set_list:
        root = ET.parse(set_file)
        set = {}
        set["name"] = root.getroot().attrib.get("name")
        set["shortName"] = root.getroot().attrib.get("shortName")
        set["cards"] = []
        for elem in root.findall("./cards/card"):
            name = elem.attrib.get('name')
            id = elem.attrib.get('id')
            number = 0
            for property in elem.findall("./property"):
                if property.attrib.get('name') == 'Number':
                    number = property.attrib.get('value')

            index = index + 1
            save_card(conn, index, id, name, number, set['name'], set['shortName'])

    conn.commit()
    conn.close()


def save_card(conn, index, id, name, card_number, set_name, set_short_name):
    sql_insert = "INSERT INTO CARDS (ID, CARD_ID, CARD_NAME, CARD_NUMBER, SET_NAME, SET_SHORT_NAME) VALUES ( {}, '{}', '{}', '{}', '{}', '{}');".format(
        index, id, name.replace("\'", "\'\'"), card_number, set_name.replace("\'", "\'\'"), set_short_name)
    # sql_insert = "INSERT INTO CARDS (ID,NAME,CARD_NUMBER, SET_NAME, SET_SHORT_NAME) VALUES ('" + id + "', '" + name.replace("\'", "\'\'") + "', '" + card_number + "', '" + set_name.replace("\'", "\'\'") +"', '" + set_short_name + "');".format(id, name, card_number, set_name, set_short_name)
    print(sql_insert)
    conn.execute(sql_insert)


save_database()

print("Database created")
