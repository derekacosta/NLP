#!/usr/bin/env python3

"""
Converts chaos.html into JSON. A sample of the input:

<xxx1><p>Dearest <i>creature</i> in <i>creation</i><br>
<xxx2>Studying English <i>pronunciation</i>,<br>
<xxx3><tt>&nbsp;&nbsp;&nbsp;</tt>I will teach you in my <i>verse</i><br>
<xxx4><tt>&nbsp;&nbsp;&nbsp;</tt>Sounds like <i>corpse</i>, <i>corps</i>, <i>horse</i> and <i>worse</i>.</p>

A hand-formatted portion of the output (note that indentation, line breaks,
order of dict entries, etc. don't matter as long as the data matches):

[
    ...
    {"stanza": 3,
     "lines": [
          {"lineId": "3-1", "lineNum": 1, "text": "Pray, console your loving poet,",
           "tokens": ["Pray", ",", "console", "your", "loving", "poet"],
           "rhymeWords": ["poet"]},
          {"lineId": "3-2", "lineNum": 2, "text": "Make my coat look new, dear, sew it!",
           "tokens": ["Make", "my", "coat", "look", "new", ",", "dear", ",", "sew", "it", "!"],
           "rhymeWords": ["sew", "it"]},
          ...
     ]},
    ...
    {"stanza": 9,
     "lines": [
          {"lineId": "9-1", "lineNum": 1, "text": "From \"desire\": desirable - admirable from \"admire\",",
           "tokens": ["From", "``", "desire", "''", ":", "desirable", "-", "admirable", "from", "``", "admire", "''", ","],
           "rhymeWords": ["admire"]},
          ...
          ...]},
]

"""



import urllib, json, requests, os, sys, pprint, re
from bs4 import BeautifulSoup
from nltk import *
from nltk.corpus import cmudict
import nltk
from collections import OrderedDict


container = []

# def hasalpha(token):
#     return # TODO: whether any character in the token is a letter

# regex that breaks an HTML line into parts: line number within the stanza, main portion, spacing
# LINE_RE = # TODO:

# TODO: read from chaos.html, construct data structure, write to chaos.json



def readfile():
  url = "http://people.cs.georgetown.edu/nschneid/cosc272/f17/a1/chaos.html"
  home = requests.get(url)
  html = BeautifulSoup(str(BeautifulSoup(home.content, "html.parser")).replace("</xxx1>", " ").replace("</xxx2>", "</xxx2></xxx1>").split('<hr/>')[0], "lxml")
  cleanfile(html)

def cleanfile(html):

  regex = r'<\/?p>|<br\/?>|<\/?xxx4>|<\/?xxx3>|<\/?xxx2>|<\/?xxx1>|<\/?tt>|\\xa0\\xa0\\xa0'

  for index, stanza in enumerate(html.findAll("xxx1")):

    split = str(str(stanza.contents).replace('[','').replace(']','').replace('-',' - ')).split("\\n")
    edit = [re.sub(regex, ' ', x).strip() for x in split]
    index+=1

    lines = []

    for Id, line in enumerate(edit):
      rhymeWords = []
      Id+=1
      lineId = str(index) + '-' + str(Id)
      text = BeautifulSoup(line, "lxml").text  
      tokens = word_tokenize(line)
      copy = word_tokenize(line)
      copy_tokens = [x.strip() for x in copy if x not in ('<', '>', 'i', '/i')]
      tokens = [x.strip().lower() for x in tokens if x != 'i' and (x.isalpha() or re.match(re.compile('[,|;|-]'), x))]

      tokens = tokens[::-1]

      if tokens[0] in (',' , ';', '-'): 
        del tokens[0]      

      if '-' in tokens[0]:
        tokens[0] = tokens[0].split('-')[1]

      if tokens[0] == 'it':
        rhymeWords.append(tokens[1])
        rhymeWords.append(tokens[0])
      else: 
        rhymeWords.append(tokens[0])

      lines.append({ "lineId" : lineId, "lineNum" : Id, "text" : text, "tokens" : copy_tokens, "rhymeWords" : rhymeWords })

    data = {"stanza" : index, "lines" : lines}
    dict(data)

def dict(data):
  container.append(data)

def ind(array):
  for i, elem in enumerate(array): 
    if elem == 'i':
      return i

def writeJSON():
  if os.path.exists("chaos.json"):
     f = file("chaos.json", "r+")
  else:
     f = file("chaos.json", "w")
  j = json.dumps(container, indent=4)
  f.write(j)
  f.close()

def main():
  readfile()  
  writeJSON()


if __name__ == "__main__":
    main()






