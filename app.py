from flask import Flask
from flask import request, jsonify
import spacy
import re


app = Flask(__name__)

def filterSpeacialChars(words):
    forbidden = ['<', '>']
    return list(i for i in words if all(c not in i for c in forbidden))

@app.route('/', methods=['POST'])
def parseData():
    nlp = spacy.load("en_core_web_sm")
    content = request.json
    doc = nlp(content['body'])

    nouns = list()
    p_nouns = list()
    nums = list()
    emails = list()
    urls = list()
    time = list()

    for token in doc:
        data = str(token.text)
        if token.pos_ == 'NOUN':
            if re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data):
                print(data)
                emails.append(data)
            elif re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data):
                urls.append(data)
            else:
                nouns.append(data)
        elif token.pos_ == 'PROPN':
            if re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data):
                urls.append(data)
            else:
                p_nouns.append(data)
        elif token.pos_ == 'NUM':
            if re.search('([0-9][0-9]:[0-9][0-9])', data) or re.search('([0-9][0-9]:[0-9][0-9]):[0-9][0-9]', data):
                time.append(data)
            else:
                nums.append(data)

        elif token.pos_ == 'X':
            if re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data):
                urls.append(data)
            elif re.search('(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data) and len(data) > 5:
                print(data)
                emails.append(data)

    result = {}
    result["noun"] = nouns
    result["pnoun"] = p_nouns
    result["num"] = nums
    result["email"] = emails
    result["url"] = urls
    result["time"] = time

    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')