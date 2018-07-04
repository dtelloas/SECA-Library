# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import aiml

"""
SECA Knowledge Module Class
"""
class KnowledgeModule(object):

	"""
	Method used to initialize the Knowledge Module
	"""
	def __init__(self):
		self.__aiml = aiml.Kernel()
		self.__known = []
	
	"""
    Returns AIML corresponding to the message parameter
    """	
	def getAIML (self, key):
		return self.__aiml.respond(key)
		
	"""
	Adds AIML file to the Knowledge Module
	"""
	def loadAIML(self, aimlFile):
		self.__aiml.learn(aimlFile)
		
	"""
	Adds certain Knowledge to the Knowledge Module
	"""
	def addKnowledge(self, knowledge):
		self.__known.append(knowledge)
		
	"""
	Returns all concepts of a certain topic
	"""	   
	def getKnowledgeList(self, topic):
		for knowledge in self.__known:
			if knowledge.getTopic() == topic:
				return knowledge.getConcepts()
		return None
		
	"""
	Returns all concepts in the Knowledge Module
	"""	    
	def getAllKnowledgeConcepts(self):
		keys = []
		for knowledge in self.__known:
			for key in knowledge.getConcepts():
				keys.append(key)
		return keys
        
"""
Knowledge Class
"""          
class Knowledge(object):

	"""
	Method used to initialize a Knowledge
	"""
	def __init__(self, topic, concepts):
		self.__topic = topic
		self.__concepts = concepts

	"""
	Returns the Knowledge topic
	"""
	def getTopic(self):
		return self.__topic
		
	"""
	Returns the list of concepts
	"""    
	def getConcepts(self):
		return self.__concepts