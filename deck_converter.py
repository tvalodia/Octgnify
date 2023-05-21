import copy
import os
import re
from xml.etree import ElementTree as ET

from octgn_card import OctgnCard
from octgn_deck import OctgnDeck


class DeckConverter:

    def __init__(self, octgn_directory, input_file, output_file):
        self.octgn_directory = octgn_directory
        self.input_file = input_file
        self.output_file = output_file

    def get_database(self):
        print("Scanning database")
        set_list = []
        for root, dirs, files in os.walk(
                self.octgn_directory + "/Data/GameDatabase/A6C8D2E8-7CD8-11DD-8F94-E62B56D89593"):
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

    def get_card_list(self):
        print("Reading card list")
        with open(self.input_file) as f:
            lines = f.read().splitlines()

        cards = []
        for line in lines:
            x = re.match(r"^(\d+)(\s)(.+)(\s\()(\w+)\)\s(\d+)\s", line)
            if x:
                card = OctgnCard(x.group(5), "", x.group(3), x.group(6), x.group(1))
                cards.append(card)
        return cards

    def create_deck(self, sets, card_list):
        cards = []
        for card in card_list:
            cards.append(self.match(card, sets))
        return cards

    def match(self, card, sets):
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
            return self.get_random(card, sets)

        #     for

    def get_random(self, card, sets):
        for set in sets:
            if set:
                for set_card in sets[set]['cards']:
                    if set_card.name == card.name:
                        found_card = set_card
                        found_card.qty = card.qty
                        print("Random " + card.name + " found")
                        return found_card

        print("Random " + card.name + " not found")

    def convert(self):
        sets = self.get_database()
        card_list = self.get_card_list()
        cards = self.create_deck(sets, card_list)
        deck = OctgnDeck(cards)
        deck.save_deck(self.output_file)
