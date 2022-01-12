#!/usr/bin/env python

from collections import Counter, defaultdict
import re
import random

def tokenize(text):

	text = re.sub('\.+', '.', text) #too many ellipses of variable length
	text = re.sub('([\.,\?\!\(\)\"\:\;])', r" \1 ", text) #add spaces around punctuation
	tokens = re.split('\s+', text)
	for t in tokens:
		try:
			if t[0] == '#':
				tokens.remove(t)
		except:
			pass
		
	return tokens

class MarkovModel:

	def __init__(self):

		self.corpus = []
		self.trigrams = Counter()
		self.database = defaultdict(list)

	def get_trigrams(self, doc):

		for i in range(len(doc)-2):

			w1, w2, w3 = doc[i], doc[i+1], doc[i+2]
			self.trigrams[(w1, w2, w3)] += 1

	def gen_database(self):

		for w1, w2, w3 in self.trigrams.keys():

			key = (w1, w2)
			self.database[key].append(w3)
		

	def generate_text(self):

		text_words = []
		sentences = 0

		while 1:

			seed = random.randint(0, len(self.corpus)-3)
			try:
				if not bool(re.match('([A-Z])', self.corpus[seed][0])):
					pass
				else:
					w1, w2 = self.corpus[seed], self.corpus[seed+1]
					break
			except IndexError:
				pass

		while 1:
			text_words.append(w1)

			if w1 in ['.', '!', '?']:
				sentences += 1

				if len(text_words) >= 4 and (random.random() < float(sentences)/3 or len(text_words) > 30):
					print(self.clean_punc(' '.join(text_words)))
					return

			try:
				w1, w2 = w2, random.choice(self.database[(w1, w2)])
			except IndexError:
				self.generate_text()

	def clean_punc(self, text):

		clean_text = re.sub(r' ([\.,\!\?\)\:\;])', r'\1', text)
		clean_text = re.sub(r'([\(]) ', r'\1', clean_text)
		return clean_text





if __name__ == "__main__":

	HMM = MarkovModel()

	with open('frasier.txt', 'r') as infile:

		raw_corpus = infile.read()

		docs = re.split(('\s\#.*\s'), raw_corpus)

		for doc in docs:

			tokenized = tokenize(doc)
			HMM.get_trigrams(tokenized)
			HMM.corpus += tokenized

		HMM.gen_database()
		HMM.generate_text()


