from io import BytesIO
from xml.etree import ElementTree as ET


class OctgnDeck:
    def __init__(self, cards):
        self.cards = cards

    def get_xml(self):
        print("Converting...")
        deck = self.get_deck_element()
        command_zone_section = self.get_section_element(deck, "Command Zone")
        self.add_card_element(command_zone_section, self.cards[0])
        main_section = self.get_section_element(deck, "Main")
        for card in self.cards[1::]:
            self.add_card_element(main_section, card)
        sideboard_section = self.get_section_element(deck, "Sideboard")
        planes_section = self.get_section_element(deck, "Planes/Schemes")
        et = ET.ElementTree(deck)

        bytes = BytesIO()
        et.write(bytes, encoding='utf-8', xml_declaration=True)
        # print(bytes.getvalue())  # your XML file, encoded as UTF-8
        return bytes.getvalue()

    def save_deck(self, output_file):
        with open(output_file, "wb") as f:
            f.write(self.get_xml())

        print("Conversion complete.")

    def get_deck_element(self):
        deck = ET.Element("deck")
        deck.set("game", "a6c8d2e8-7cd8-11dd-8f94-e62b56d89593")
        return deck

    def get_section_element(self, parent, name):
        section = ET.SubElement(parent, "section")
        section.set("name", name)
        section.set("shared", "False")
        return section

    def add_card_element(self, section, card):
        card_element = ET.SubElement(section, "card")
        card_element.set("qty", card.qty)
        card_element.set("id", card.id)
        card_element.text = card.name
        return card_element
