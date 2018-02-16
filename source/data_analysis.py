import pandas as pd
import csv
import collections
import spacy
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


grammar = r'''NNP:{<NNP|NNPS|NN|NNS>+(<,|/>?<NNP|NNPS|NN|NNS>+)*}
            OTHERS : {<CD>|<JJ>|<JJR>|<JJS>|<PRP>|<PRP$>|<RB>|<RBR>|<RBS>|<SYM>|<VB>|<VBD>|<VBG>|<VBN>|<VBP>|<VBZ>|<WDT>|<WP>|<WRB>}
'''
cp_grammar = nltk.RegexpParser(grammar)

def modified_document_collection_word(list_doc,model):
	'''
	Args: list_doc,model
			list_doc: list of job descriptions available in the dataset
			model : Spacy Model for English language

	Return: A list containing modified document
	'''
	list_mod_doc = []
	for each in list_doc:
		doc = model(each)
		list_words = []
		for sent in doc.sents:
			for word in sent:
				if word.tag_ in ["NNP","NNPS","NN","NNS"]:
					list_words.append(word.text)
		list_mod_doc.append(" ".join(list_words))

	return list_mod_doc

def vectorize(corpus):
	'''
	Args: corpus
			corpus : List of modified documents containing only nouns

	Return: return tokenized words with count of the word occurrences in text documents and vocabulary to id mapping
	'''
	vectorizer = CountVectorizer()
	X = vectorizer.fit_transform(corpus)
	X.toarray()
	return X,vectorizer.vocabulary_

def compute_tfidf(X,vocab,data):
	'''
	Args: X
			X: X is an array containing tokenized words and their frequency in each document
			vocab: Mapping of words and ids

	Return: TF-IDF score of each word in document

	'''
	transformer = TfidfTransformer(smooth_idf=False)
	tfidf = transformer.fit_transform(X)
	tfidf = tfidf.toarray()
	print(vocab)
	for i in range(len(tfidf)):
		print(data[i])
		for j in range(len(tfidf[i])):
			# print(vocab[list(tfidf[i]).index(max(tfidf[i]))],max(tfidf[i]))
			if tfidf[i][j]>0.05 and tfidf[i][j]<0.2:
				print(vocab[j],tfidf[i][j])
		input()
				# print(every[1])
				# print(vocab[every[0][1]],each[1])

if __name__ == "__main__":
	list_jobs = []
	model = spacy.load("en")
	# data = pd.read_csv("../data/TrainData.csv")
	headers = ['id','job_profile','job_desc','category']
	data = pd.read_csv("../data/TrainData.csv", names = headers,quotechar="|")
	corpus = modified_document_collection_word(data['job_desc'],model)
	X,vocab = vectorize(corpus)
	vocab = {v: k for k, v in vocab.items()}
	compute_tfidf(X,vocab,data['job_desc'])
	# print(collections.Counter(data['job_profile']))
	# print(collections.Counter(data['category']))
	# for each in data['job_desc']:
	# 	print(each)
	# 	doc = model(each)
	# 	sentence = []
	# 	for sent in doc.sents:
	# 		for word in sent:
	# 			sentence.append((word.text,word.tag_))
	# 	tree = cp_grammar.parse(sentence)

	# 	for subtree in tree.subtrees():
	# 		if subtree.label() == "NNP" or subtree.label() == "NP":
	# 			print(subtree.leaves())
	# 	input()


	# with open("../data/TrainData.csv",'r') as csvfile:
	# 	data = csv.reader(csvfile,delimiter=',',quotechar='|')
	# 	for row in data:
	# 		job_desc = {}
	# 		job_desc['id'] = row[0]
	# 		job_desc['job_profile'] = row[1]
	# 		job_desc['job_desc'] = row[2]
	# 		job_desc['skills'] = row[3]
	# 		list_jobs.append(job_desc)

	# print(list_jobs[0])

