import os
from xml.etree import ElementTree as ET
import json
import re
import copy

from octgn_card import OctgnCard
from octgn_deck import OctgnDeck

GAME_DATABASE = "E:/Games/Octgn/Data/GameDatabase/A6C8D2E8-7CD8-11DD-8F94-E62B56D89593"
INPUT_FILE = "ninjitsu.txt"
OUTPUT_FILE = "ninjistu.o8d"


def get_database():
    print("Scanning database")
    set_list = []
    database = {}
    for root, dirs, files in os.walk(GAME_DATABASE):
        for file in files:
            if file.endswith(".xml"):
                set_list.append(os.path.join(root, file))
    print(len(set_list))

    sets = {}
    for set_file in set_list:
        # print (set)
        root = ET.parse(set_file)
        set = {}
        set["name"] = root.getroot().attrib.get("name")
        set["shortName"] = root.getroot().attrib.get("shortName")
        set["cards"] = []
        for elem in root.findall("./cards/card"):
            name = elem.attrib.get('name')
            id = elem.attrib.get('id')
            for property in elem.findall("./property"):
                if property.attrib.get('name') == 'Number':
                    number = property.attrib.get('value')
            card = OctgnCard(set["shortName"], id, name, number, 0)
            set["cards"].append(card)
        sets[set["shortName"]] = set

    # with open("sets.json", "w") as fp:
    #     json.dump(sets, fp)

    return sets
    # print (sets)


def get_card_list():
    print("Reading card list")
    with open(INPUT_FILE) as f:
        lines = f.read().splitlines()

    cards = []
    for line in lines:
        x = re.match(r"^(\d+)(\s)(.+)(\s\()(\w+)\)\s(\d+)\s", line)
        if x:
            card = OctgnCard(x.group(5), "", x.group(3), x.group(6), x.group(1))
            cards.append(card)
    return cards


def create_deck(sets, card_list):
    cards = []
    for card in card_list:
        cards.append(match(card, sets))
    return cards


def match(card, sets):
    if card.set_short_name.lower() in sets:
        set_cards = sets[card.set_short_name.lower()]["cards"]
        if set:
            for set_card in set_cards:
                if set_card.number == card.number.zfill(3):
                    found_card = copy.deepcopy(set_card)
                    found_card.qty = card.qty
                    return found_card
            print("Exact " + card.name + " not found")
    else:
        print(card.set_short_name + ' not found')
        return get_random(card, sets)

    #     for 


def get_random(card, sets):
    found_card = {}
    for set in sets:
        if set:
            for set_card in sets[set]['cards']:
                if set_card.name == card.name:
                    found_card = set_card
                    found_card.qty = card.qty
                    print("Random " + card.name + " found")
                    return found_card

    print("Random " + card.name+ " not found")


sets = get_database()
card_list = get_card_list()
cards = create_deck(sets, card_list)
deck = OctgnDeck()
deck.save_deck(cards, OUTPUT_FILE)
