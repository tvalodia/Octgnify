import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')

from flask import Flask, request, Response
from deck_converter import DeckConverter

ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)


@app.route('/x')
def hello():
    return 'Hello, World!'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/convert', methods=['POST'])
def convert_input_deck():
    deck_converter = DeckConverter('E:\\Games\\Octgn')
    payload = request.json
    filename = payload['filename']
    deck = payload['deck']
    output_deck = deck_converter.convert(deck)
    return Response(
        output_deck.get_xml().decode('utf-8'),
        mimetype='text/plain',
        headers={'Content-disposition': 'attachment; filename=hello.txt'})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")


if __name__ == '__main__':
    app.run(debug=True)
