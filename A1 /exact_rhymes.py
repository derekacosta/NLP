#!/usr/bin/env python3

import json, re, os 	
from collections import defaultdict
from nltk.corpus import cmudict # need to have downloaded the data through NLTK
from  __builtin__ import any as b_any
import math

def isExactRhyme(p1, p2):
    """
    TODO: Explain your heuristic here.

    I first attempted to do some evaluation of the list length and reassign them based on length for easy of processing. 

    Once that is done I iterate through the first list, separate it as to retrieve the inner list, and split it by space for later processing. This is again repeated for the second list. 

   	Afterwards, it attempted to match the components of the first list to the second and collect the amount of terms they share in common. 

   	Finally, it compares the lenght of matches to that of the average for the smallest list and registers if its larger or equal in length then the accurate and potential of it being a ryhming couplet holds and returns true. 

    """
    if len(p1) > len(p2):
    	if p1 and p2: 
	    	if len(p1[0]) > len(p2[0]): 
		    	p3 = p1
		    	p1 = p2
		    	p2 = p3

    for i in p1: 
		j = i.split(' ')
		matches = []
		for k in j:
			for l in p2: 
				m = l.split(' ') 
				if k in m: 
					matches.append(k)
		return len(matches) >= math.ceil(len(j)/2)


# Load chaos.pron.json
with open('chaos.pron.json') as f:    
    data = json.load(f)

# For each pair of lines that are supposed to rhyme,
# check whether there are any pronunciations of the words that
# make them rhyme according to cmudict and your heuristic.
# Print the rhyme words with their pronunciations and whether
# they are deemed to rhyme or not
# so you can examine the effects of your rhyme detector.
# Count how many pairs are deemed to rhyme vs. not.


count_no_prons = 0
count_with_prons = 0
rhyming_pairs = 0
no_rhyming_pairs = 0

for index, i in enumerate(data):
	pair = []
	for ind, j in enumerate(data[index]["lines"]):
		rhyme = data[index]["lines"][ind]["rhymeWords"]

		prons = []
		if data[index]["lines"][ind]["rhymeProns"]: 
			prons = data[index]["lines"][ind]["rhymeProns"][0]
	
		pair.append(prons)
		if len(pair) is 2: 
			# print pair[0], pair[1]
			# print isExactRhyme(pair[0], pair[1])
			if isExactRhyme(pair[0], pair[1]):
				rhyming_pairs+=1
			else: 
				no_rhyming_pairs+=1

			if not pair[0] or  not pair[1]: 
				count_no_prons+=1
			else:
				count_with_prons+=1

			pair = []		

		# print prons
		
		# for x, k in enumerate(rhyme):
		# 	prons = []
		# 	for key, value in spare: 
		# 		if re.match(re.compile(rhyme[x].lower() + '$'), key.lower()): 
		# 			prons.append(value)
		# 	# prons.append([value for key, value in spare if re.match(re.compile(rhyme[x] + '$'), key)])	 
		# 	if not prons: 		
		# 		OOV.append(rhyme[x].lower())
		# 	data[index]["lines"][ind]["rhymeProns"] = prons
print("no rhyming pronunciations: " + str(count_no_prons))
# print "rhyming pronunciations: " + str(count_with_prons)
print("ryhming_pairs: " + str(rhyming_pairs))
print("no ryhming_pairs: " + str(no_rhyming_pairs))

"""
TODO: Answer the questions briefly:

- How many pairs of lines that are supposed to rhyme actually have rhyming pronunciations
according to your heuristic and cmudict?

	115

- For how many lines does having the rhyming line help you disambiguate
between multiple possible pronunciations?

	
	105 

- What are some reasons that lines supposed to rhyme do not,
according to your rhyme detector? Give examples. What are some reasons that your heuristic is imperfect?

	Either the cmudict does not contain them, or the library has not been updated in a while or the pronoucation added extra characters I was not aware of or algorithm is incorrect. But the biggest reason is largely because the amount of edge cases and some phrases of word cut it short when it comes to rhyming.  
		for instance comparing 

		[u'P OW1 AH0 T'] [u'S OW1' 'IH0 T' ]
			poet 			sew it 	

		these have two different forms and it difficult to check for 

	My heuristic is imperfect because of the number of edge case possible, but it seems to have worked out pretty well 
...

"""