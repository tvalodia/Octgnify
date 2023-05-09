from io import BytesIO
import os
from xml.etree import ElementTree as ET
import json
import re
import copy

GAME_DATABASE = "E:/Games/Octgn/Data/GameDatabase/A6C8D2E8-7CD8-11DD-8F94-E62B56D89593"
INPUT_FILE = "ninjitsu.txt"
OUTPUT_FILE = "ninjistu.o8d"

def get_database():
    print ("Scanning database")
    set_list = []
    database = {}
    for root, dirs, files in os.walk(GAME_DATABASE):
        for file in files:
            if file.endswith(".xml"):
                set_list.append(os.path.join(root, file))
    print (len(set_list))

    sets = {}
    for set_file in set_list:
        # print (set)
        root = ET.parse(set_file)
        set = {}
        set["name"] = root.getroot().attrib.get("name")
        set["shortName"] = root.getroot().attrib.get("shortName")
        set["cards"] = []
        for elem in root.findall("./cards/card"):
            card = {}
            name = elem.attrib.get('name')
            id = elem.attrib.get('id')
            for property in elem.findall("./property"):
                if property.attrib.get('name') == 'Number':
                    number = property.attrib.get('value')
            # print (name + " - " +  id)
            card = {"name": name, "id": id, "number": number}
            set["cards"].append(card)
        sets[set["shortName"]] = set
    

    with open("sets.json", "w") as fp:
        json.dump(sets,fp) 

    return sets
    # print (sets)



def get_card_list():
    print ("Reading card list")
    lines = []
    with open(INPUT_FILE) as f:
        lines = f.read().splitlines()
    
    cards = []
    for line in lines:
        card = {}
        x = re.match(r"^(\d+)(\s)(.+)(\s\()(\w+)\)\s(\d+)\s", line)
        if x:
            card["count"] = x.group(1)
            card["name"] = x.group(3)
            card["set"] = x.group(5)
            card["number"] = x.group(6)
            cards.append(card)
    
    return cards

def create_deck(sets, card_list):
    cards = []
    for card in card_list:
        cards.append(match(card, sets))
    return cards

def match(card, sets):
    if card["set"].lower() in sets:
        set_cards = sets[card["set"].lower()]["cards"]
        found_card = {}
        if set:
            for set_card in set_cards:
                if set_card['number'] == card['number'].zfill(3):
                    found_card = copy.deepcopy(set_card)
                    found_card['qty'] = card['count']
                    return found_card
            print ("Exact " + card['name'] + " not found")
    else:
        print (card['set'] + ' not found')
        return get_random(card, sets)

    #     for 

def get_random(card, sets):
    found_card = {}
    for set in sets:
        if set:
            for set_card in sets[set]['cards']:
                if set_card['name'] == card['name']:
                    found_card = set_card
                    found_card['qty'] = card['count']
                    print ("Random " + card['name'] + " found")
                    return found_card
        
    print ("Random " + card['name'] + " not found")


def save_deck(cards):
    print ("Converting...")
    deck = get_deck_element()
    command_zone_section = get_section_element(deck, "Command Zone")
    add_card_element(command_zone_section, cards[0])
    main_section = get_section_element(deck, "Main")
    for card in cards[1::]:
        add_card_element(main_section, card)
    sideboard_section = get_section_element(deck, "Sideboard")
    planes_section = get_section_element(deck, "Planes/Schemes")
    et = ET.ElementTree(deck)

    bytes = BytesIO()
    et.write(bytes, encoding='utf-8', xml_declaration=True) 
    # print(bytes.getvalue())  # your XML file, encoded as UTF-8
     
    # Opening a file under the name `items2.xml`,
    # with operation mode `wb` (write + binary)
    with open(OUTPUT_FILE, "wb") as f:
        f.write(bytes.getvalue())

    print ("Conversion complete.")

def get_deck_element():
    deck = ET.Element("deck")
    deck.set("game", "a6c8d2e8-7cd8-11dd-8f94-e62b56d89593")
    return deck

def get_section_element(parent, name):
    section = ET.SubElement(parent, "section")
    section.set("name", name)
    section.set("shared", "False")
    return section

def add_card_element(section, card):
    card_element = ET.SubElement(section, "card")
    card_element.set("qty", card['qty'])
    card_element.set("id",card['id'])
    card_element.text = card['name']
    return card_element

sets = get_database()
card_list = get_card_list()
deck = create_deck(sets, card_list)
save_deck(deck)
