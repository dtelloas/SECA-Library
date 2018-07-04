# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random

"""
SECA Personality Module Class
"""
class PersonalityModule(object):

	"""
	Method used to initialize the Personality Module
	"""
	def __init__(self, initialM, initialE, moodM, emotionM, meprobM):
		#We start with neutral mood
		self.__mood = initialM
		self.__emotion = initialE
		
		#Mood and Emotion Transition matrices
		self.__moodMatrix = moodM
		self.__emotionMatrices = emotionM
		self.__meprobM = meprobM
		
	"""
	Method used to compute the update of the mood or emotion
	"""
	def compute(self, probs, ratio, matrix, mood):
		prob = []
		for element in matrix:
			aux = []
			for i in range(3):
				num = (1-ratio)*element[i]+ratio*probs[i]
				aux.append(num)
			prob.append(aux)
			
		#Results are normalized
		if mood==0:
			norm = [float(i)/sum(prob[self.__emotion]) for i in prob[self.__emotion]]
		else:
			norm = [float(i)/sum(prob[self.__mood]) for i in prob[self.__mood]]
			
		#Intervals are calculated
		intervals = []
		aux = 0
		for i in norm:
			intervals.append((aux, aux+i))
			aux += i
			
		#New mood or emotion is chosen randomly given the intervals
		epsilon = random.random()
		count = 0
		for interval in intervals:
			if epsilon > interval[0] and epsilon < interval[1]:
				return count
			else:
				count += 1
				
	"""
	Method to update the Personality Module
	"""
	def update(self, probs):
		self.__emotion = self.compute(probs, 0.4, self.__emotionMatrices[self.__mood], 0)
		self.__mood = self.compute(self.__meprobM[self.__emotion], 0.2, self.__moodMatrix, 1)
		
	"""
	Returns the current mood
	"""
	def getMood(self):
		return self.__mood
		
	"""
	Returns the current emotion
	"""
	def getEmotion(self):
		return self.__emotion
		
	"""
	Sets the current mood
	"""        
	def setMood(self,mood):
		self.__mood = mood
		
	"""
	Sets the current mood
	"""
	def setEmotion(self,emotion):
		self.__emotion = emotion