from deck_converter import DeckConverter


class DeckFileConverter:

    def __init__(self, octgn_directory, input_file, output_file):
        self.deck_converter = DeckConverter(octgn_directory)
        self.deck_converter.add_listener(self)
        self.input_file = input_file
        self.output_file = output_file
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def message(self, message):
        for listener in self.listeners:
            listener.on_message(message)

    def on_start(self):
        pass

    def on_complete(self):
        pass

    def on_message(self, message):
        self.message(message)

    def convert(self):
        self.message("Reading input deck")

        with open(self.input_file) as f:
            lines = f.read()
        deck = self.deck_converter.convert(lines)
        deck.save_deck(self.output_file)

        for listener in self.listeners:
            listener.on_complete()
