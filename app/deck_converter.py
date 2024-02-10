import os.path
import re
import sqlite3

from octgn_card import OctgnCard
from octgn_deck import OctgnDeck


class DeckConverter:

    def __init__(self, octgn_directory):
        self.octgn_directory = octgn_directory
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def get_card_list(self, deck):
        self.message("Creating input deck from input data")
        lines = deck.splitlines()

        cards = []
        for line in lines:
            x = re.match(r"^(\d+)(?:\s)(.+?)(?:\s\/\/\s.+)?(?:\s\()(\w+)(?:\))(?:\s)((?:\w*-)*\d+)\s*", line)
            if x:
                card = OctgnCard(x.group(3), "", x.group(2), x.group(4), x.group(1))
                cards.append(card)
        return cards

    def create_deck(self, card_list):
        cards = []
        for card in card_list:
            cards.append(self.match(card))
        return cards

    def match(self, card):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "octgn.db")
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            sql = "SELECT CARD_ID, CARD_NAME, CARD_NUMBER, SET_NAME, SET_SHORT_NAME from CARDS" \
                  " WHERE LOWER(SET_SHORT_NAME) = '{}'" \
                  " AND CARD_NUMBER = '{}';" \
                .format(card.set_short_name.lower(), card.number.zfill(3))
            result = cursor.execute(sql)
            data = result.fetchone()

            if data:
                card_id, card_name, card_number, set_name, set_short_name = data
                self.message("Exact " + card.name + " found")
                return OctgnCard(set_short_name, card_id, card_name, card_number, card.qty)
            else:
                result = cursor.execute(
                    "SELECT CARD_ID, CARD_NAME, CARD_NUMBER, SET_NAME, SET_SHORT_NAME from CARDS"
                    " WHERE LOWER(CARD_NAME) = '{}';".format(card.name.lower().replace("\'", "\'\'")))

                card_id, card_name, card_number, set_name, set_short_name = result.fetchone()
                if card_id:
                    self.message("Random " + card.name + " chosen from Octgn database")
                    return OctgnCard(set_short_name, card_id, card_name, card_number, card.qty)

    def convert(self, inputText):
        for listener in self.listeners:
            listener.on_start()

        card_list = self.get_card_list(inputText)
        cards = self.create_deck(card_list)
        deck = OctgnDeck(cards)

        for listener in self.listeners:
            listener.on_complete()

        return deck

    def message(self, message):
        for listener in self.listeners:
            listener.on_message(message)


class DeckConverterListener:

    def on_start(self):
        pass

    def on_complete(self):
        pass

    def on_message(self, message):
        pass
