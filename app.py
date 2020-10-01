from flask import Flask
from flask import request, jsonify
import spacy
import re
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

nlp = spacy.load("en_core_web_sm")

@app.route('/test', methods=['POST'])
@cross_origin()
def parseBody():
    content = request.json
    content = content["body"]
    response = parseData(str(content))
    return jsonify(response)

def parseData(data):
    doc = nlp(data)

    nouns = list()
    p_nouns = list()
    nums = list()
    phone = list()
    emails = list()
    time = list()
    names = list()
    loc = list()
    org = list()
    urls = list()

    for token in doc:
        data = str(token.text)
        if len(data) > 1:
            if token.pos_ == 'NOUN':
                if re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data):
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
                print(token)
                if re.search('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', data) and len(data) > 5:
                    emails.append(data)
                elif re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data):
                    urls.append(data)


    for ent in doc.ents:
        data = str(ent.text)
        if ent.label_ == 'PERSON':
            if re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data):
                emails.append(data)
            else:
                d = data.replace('\r', '')
                d = d.replace('\n', '')
                names.append(d)
        elif ent.label_ == 'GPE':
            loc.append(data)
        elif ent.label_ == 'ORG':
            org.append(data)

    result = {}
    result["noun"] = list(dict.fromkeys(nouns))
    result["name"] = list(dict.fromkeys(names))
    result["pnoun"] = list(dict.fromkeys(p_nouns))
    result["num"] = list(dict.fromkeys(nums))
    result["email"] = list(dict.fromkeys(emails))
    result["url"] = list(dict.fromkeys(urls))
    result["time"] = list(dict.fromkeys(time))

    return result

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)