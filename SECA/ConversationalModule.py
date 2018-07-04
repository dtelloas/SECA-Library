# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from FiniteStateMachine import *
import random

"""
SECA Conversational Module Class
"""
class ConversationalModule(object):

	"""
	Method used to initialize the Conversational Module
	"""
	def __init__(self):
		self.__currentConversation = None
		self.__conversationsDict = {}

	"""
	Returns true if there is a conversation going on
	"""
	def isConversationSelected(self):
		return self.__currentConversation != None
		
	"""
	Adds a conversation to the Conversational Module
	"""
	def addConversation(self, conv):
		self.__conversationsDict[conv.getID()] = conv
		
	"""
	Returns the ID of the current conversation or inner Dialog (if exists)
	"""        
	def getInnerDialogID(self):
		if self.__currentConversation!=None:
			id = self.__currentConversation.getInnerCModelID()
			if id!=None:
				return id
			else:
				return self.__currentConversation.getName()
		else:
			return None
			
	"""
	Returns the ID of the current inner State
	"""     
	def getInnerStateID(self):
		if self.__currentConversation!=None:
			return self.__currentConversation.getInnerStateID()
		else:
			return None
			
	"""
	Updates the Conversational Module
	"""
	def update(self, convID, params = None):
		
		if self.__currentConversation == None:
			self.__currentConversation = self.__conversationsDict[convID]
			
		keys = self.__currentConversation.update(params)
		if self.__currentConversation.isCompleted():
			self.__currentConversation.restart()
			self.__currentConversation = None
			
		return keys
		
	"""
	Cancels the current conversation of the Conversational Module
	""" 
	def cancel(self):
		if self.__currentConversation != None:
			self.__currentConversation.restart()
			self.__currentConversation = None
			
	"""
	Returns all keywords in inner Dialogs (if exist)
	"""         
	def getKeywords(self):
		keys = []
		for conv in self.__conversationsDict.values():
			for key in conv.getAllInnerKeyWords():
				keys.append(key)
		return keys
		
	"""
	Returns the ID of the Dialog that matches with some Keywords
	"""
	def getMatchDialogID(self,words):
		wordsS = " "
		for word in words:
			wordsS+=word+" "
		for conv in self.__conversationsDict.values():
			id = conv.checkInnerDialogID(wordsS)
			if id!=None:
				return id
		return None


"""
ConversationalModel Class
Though conceptually Conversations and Dialog Types represent different things, 
the code structure is the same for both. Consequently, ConversationalModel class
can be used to implement everything
"""
class ConversationalModel(object):

	"""
	Method used to initialize a Conversational Model (CM)
	"""
	def __init__(self, name = None, ID = None, keyWords = []):
		self.__name = name #Name of the CM
		self.__ID = ID #Numeric ID of the CM
		self.__keyWords = keyWords #Keywords that can be used to identify the CM
		self.__FSM = FiniteStateMachine() #State machine that defines the CM
		
	"""
	Returns the ID of the CM
	"""
	def getID(self):
		return self.__ID
		
	"""
	Returns the name of the CM
	"""
	def getName(self):
		return self.__name
		
	"""
	Returns the keywords of the CM
	"""      
	def getKeyWords(self):
		return self.__keyWords
		
	"""
	Method used to add a state to the CM
	"""
	def addState(self,state):
		self.__FSM.add_state(state)
		
	"""
	Updated the FSM of the CM
	""" 
	def update(self, params = None):
		return self.__FSM.run(params)
		
	"""
	Returns true if the CM is completed
	""" 
	def isCompleted(self):
		return self.__FSM.isCompleted()
		
	"""
	Restarts the CM
	""" 
	def restart(self):
		self.__FSM.restart()
		
	"""
	Returns the name of the inner CM
	"""  
	def getInnerCModelID(self):
		model = self.__FSM.get_innerCModelID()
		if model!=None:
			return model
		else:
			return self.__name
	
	"""
	Returns the ID of the current state or inner DT (if exists) state
	"""  
	def getInnerStateID(self):
		return self.__FSM.get_innerStateID()
		
	"""
	Returns the keywords of all inner CM
	"""
	def getAllInnerKeyWords(self):
		keys = []
		for key in self.__keyWords:
			keys.append(key)
		for key in self.__FSM.get_innerKeywords():
			keys.append(key)
		return keys
		
	"""
	Returns the name of the inner CM with matching keywords
	"""
	def checkInnerCModelID(self, words):
		keys = self.getKeyWords()
		for key in keys:
			if key in words:
				return self.__taskID
		return self.__FSM.check_innerCModelID(words)
		
	"""
	Sets the current state of the FSM
	"""
	def setCurrState(self,stateID):
		self.__FSM.set_current(stateID)