import re

pronDict = {}
done_sets = []

with open('2of12.txt', 'r', encoding='utf-8') as filtList:

	common_words = []

	for line in filtList:

		line = re.sub('[0-9\n]+','',line)
		common_words.append(line)

	filtList.close()

with open('cmudict-0.7b', 'r', encoding='utf-8', errors='ignore') as cmu:

	counter = 0

	for line in cmu:

		splitLine = line.split(' ')
		
		for i in range(len(splitLine)):

			splitLine[i] = re.sub('[0-9()\n]+', '', splitLine[i])

		word = splitLine[0]

		if word.lower() in common_words:

			pronunciation = tuple(splitLine[2:])
			pronDict[pronunciation] = word

	cmu.close()



with open('spoonerisms.txt', 'w') as out:

	count = 0

	for pron1 in pronDict.keys():

		onset1 = pron1[0]
		restOfWord1 = pron1[1:]

		for pron2 in pronDict.keys():

			onset2 = pron2[0]
			restOfWord2 = pron2[1:]

			if not onset1 == onset2 and not restOfWord1 == restOfWord2:

				pron3 = tuple(onset2) + restOfWord1
				pron4 = tuple(onset1) + restOfWord2


				try:

					if pron3 in pronDict.keys() and pron4 in pronDict.keys():


						wordset = set([pron1,pron2,pron3,pron4])

						if not wordset in done_sets:

							count += 1
							print("Spoonerisms found: %s" % str(count))

							done_sets.append(wordset)
							spoonerism = pronDict[pron1]+' '+pronDict[pron2]+' '+pronDict[pron3]+' '+pronDict[pron4]+'\n'

							out.write(spoonerism)
				except:
					pass

	out.close()




