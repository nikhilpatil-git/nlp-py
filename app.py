from flask import Flask
from flask import request, jsonify
import spacy

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def parseData():
    nlp = spacy.load("en_core_web_sm")
    content = request.json
    doc = nlp(content['body'])

    nouns = list()
    p_nouns = list()
    nums = list()

    for token in doc:
        if token.pos_ == 'NOUN':
            nouns.append(token.text)
        elif token.pos_ == 'PROPN':
            p_nouns.append(token.text)
        elif token.pos_ == 'NUM':
            nums.append(token.text)

    result = {}
    result["Noun"] = nouns
    result["PNoun"] = p_nouns
    result["Num"] = nums

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')