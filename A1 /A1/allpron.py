#!/usr/bin/env python3

import json, re, os
from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import cmudict # need to have downloaded the data through NLTK
import nltk

""" Sample part of the output (hand-formatted):

{"lineId": "3-2", "lineNum": 2,
 "text": "Make my coat look new, dear, sew it!",
 "tokens": ["Make", "my", "coat", "look", "new", ",", "dear", ",", "sew", "it", "!"],
 "rhymeWords": ["sew", "it"],
 "rhymeProns": [["S OW1"], ["IH1 T", "IH0 T"]]
},
"""

# Load the cmudict entries into a data structure.
# Store each pronunciation as a STRING of phonemes (separated by spaces).

# nltk.download("cmudict")
entries = cmudict.entries()

spare = defaultdict(list)
for key, value in entries: 
	value = ' '.join(value)
	spare[key].append(value)
	

# Load chaos.json
with open('chaos.json') as f:    
    data = json.load(f)

# For each line of the poem, add a "rhymeProns" entry
# which is a list parallel with "rhymeWords".
# For each word, it contains a list of possible pronunciations.

OOV = []
for index, i in enumerate(data):
	for ind, j in enumerate(data[index]["lines"]):
		rhyme =  data[index]["lines"][ind]["rhymeWords"]
		prons = []
		for x, k in enumerate(rhyme):
			if spare.has_key(rhyme[x].lower()):
				prons.append(spare[rhyme[x].lower()])
			else: 
				OOV.append(rhyme[x].lower())

			data[index]["lines"][ind]["rhymeProns"] = prons


print len(OOV), OOV

# Write the enhanced data to chaos.pron.json
if os.path.exists("chaos.pron.json"):
	f = file("chaos.pron.json", "w")
else:
    f = file("chaos.pron.json", "w")

j = json.dumps(data, indent=4)
f.write(j)
f.close()

"""
TODO: Answer the question:

- How many rhyme words are NOT found in cmudict (they are "out-of-vocabulary", or "OOV")?
Give some examples.

******************************************************
ANSWER:
There are 24 rhyme words that are not found in cmudict ~ OOV 

all the ones found: 

 24 [u'ague', u'terpsichore', u'reviles', u'endeavoured', u'tortious', u'davit', u'clamour', u'clangour', u'hygienic', u'inveigle', u'pshaw', u'mezzotint', u'cholmondeley', u'antipodes', u'obsequies', u'dumbly', u'streatham', u'oppugners', u'tuners', u'victual', u'deafer', u'vapour', u'fivers', u'gunwale']

******************
...
"""

