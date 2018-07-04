# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial
from ..models import *
import time
import datetime

"""
SECA NLP Module Class
"""
class NLPModule(object):

	"""
	Method used to initialize the NLP Module
	"""
	def __init__(self):
		self.__models = {}
		self.__kmfunctions = {}
		self.__values = {}
		self.__maxPThresh = {}
		self.__checkLastKW = {}
		self.__firstKW = {}
		self.__cleaning = None
		self.__spellCheck = None
		self.__embedding = None
		
	"""
	Method used to load a cleaning function
	"""
	def loadCleaningF(self,cleanF):
		self.__cleaning = partial(cleanF)
		
	"""
	Returns clean text using the cleaning function
	"""
	def cleaning(self,text):
		if self.__cleaning==None:
			return text
		else:
			cleanT = self.__cleaning(text)
			return cleanT
			
	"""
	Method used to load a spellcheck function
	"""
	def loadSpellCheckF(self,scF):
		self.__spellCheck = partial(scF)
		
	"""
	Returns the words returned by the spellcheck function
	""" 
	def spellCheck(self,word):
		if self.__spellCheck==None:
			return word
		else:
			scW = self.__spellCheck(word)
			return scW
			
	"""
	Method used to load an embedding function
	"""			
	def loadEmbeddingF(self,embF,mod):
		self.__embedding = partial(embF,model=mod,spellCheckF=self.__spellCheck)
		
	"""
	Returns the list of features associated with a list of words
	"""	
	def embedding(self,words):
		if self.__embedding==None:
			return words
		else:
			embW = self.__embedding(words)
			return embW
	
	"""
	Function to load a model in the NLP Module
	"""	
	def loadModel(self, type, model, kmfunction, values, maxPThresh,checkLast,firstkw):
		self.__models[type] = model
		if kmfunction !=None:
			self.__kmfunctions[type] = partial(kmfunction)
		else:
			self.__kmfunctions[type] = None
		self.__values[type] = values
		self.__maxPThresh[type] = maxPThresh
		self.__checkLastKW[type] = checkLast
		self.__firstKW[type] = firstkw
		
	"""
	Returns a list with preprocessed words of a certain text (1) and its embedding(0)
	"""
	def preprocessing(self,text):
		cleanT = self.cleaning(text)
		results = self.embedding(cleanT)
		return results #0 is Features, 1 is words
		
	"""
	Returns the classification result of a certain type of a message
	"""
	def classification(self, type, words, feat, message):
		startT = time.time()
		model = self.__models.get(type)
		kmfunction = self.__kmfunctions.get(type)
		if self.__firstKW[type] and kmfunction!=None:
			print type+" KEYWORDS FIRST"
			predRes = kmfunction(words)
			endT = time.time()
			self.saveNLPData(message,words,type+" KEYWORDS FIRST",predRes[0],[0],endT-startT)
			if predRes[1]==True:
				return predRes[0]
		predProb = model.predict_proba([feat])
		maxP = max(predProb[0])
		val = self.__values[type]
		if maxP>self.__maxPThresh[type]: #Machine Learning
			idx = predProb[0].tolist().index(maxP)
			if self.__checkLastKW[type] and idx==len(predProb[0].tolist())-1:
				print type+" MACHINE LEARNING AND END KEYWORDS"
				predRes = kmfunction(words)
				endT = time.time()
				self.saveNLPData(message,words,type+" MACHINE LEARNING AND END KEYWORDS",predRes[0],[0],endT-startT)
				return predRes[0]
			else:
				print type+" MACHINE LEARNING"
				predRes = val[idx]
				endT = time.time()
				self.saveNLPData(message,words,type+" MACHINE LEARNING",predRes,predProb[0],endT-startT)
				return predRes
		elif kmfunction!=None: #Keywords
			print type+" KEYWORDS"
			predRes = kmfunction(words)
			endT = time.time()
			self.saveNLPData(message,words,type+" KEYWORDS",predRes[0],[0],endT-startT)
			return predRes[0]
		return None
		
	"""
	Method to save NLP related data
	"""
	def saveNLPData(self,message,words,type,result,MLprob,elapsedTime):
		nlp_data = ClassificationData()
		if message==None:
			message = ""
		nlp_data.message = message
		wordsS = ""
		if words==None:
			wordsS = ""
		else:
			for word in words:
				wordsS+=word+";"
		nlp_data.processedWords = wordsS
		nlp_data.classificationType = type
		probsS = ""
		for prob in MLprob:
			probsS+=str(prob)+";"
		nlp_data.MLprobabilities = probsS
		if result==None:
			result = ""
		nlp_data.classResult = result
		nlp_data.processTime = elapsedTime
		nlp_data.timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S')
		nlp_data.save()
    	