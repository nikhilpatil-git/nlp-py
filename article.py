# Import the spacy library
import spacy
import re

# Load the pre-trained statistical model
nlp = spacy.load("en_core_web_sm")

# Join the email lines into single text.
doc = nlp("From Gerry Kreese Sent: Friday 13, September 2019 09:12 To: customerservices@abc.ie Subject: Display issue with tv screen Hello ABC, My name is Gerry Kreese and I bought a Sony tv from your Philadelphia center last Sunday and I'm facing some display issue with the screen. Can you please send someone to fix it. I live just across the 203 Christopher Columbus Blvd, Philadelphia and for any other query you can contact me at +12676781822. Thanks Gerry Kreese")

# List to store all the proper-nouns
pii = list()

mob_regex = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# Loop through each word to determine it's POS and filter the
# ones which are Proper-Nouns
for token in doc:
    if token.pos_ == 'PROPN':
        pii.append(token.text)
    elif re.search(mob_regex, str(token)):
        pii.append(token.text)
    elif re.search(email_regex, token.text):
        pii.append(token.text)

# Print all the unique proper-nouns
print(set(pii))