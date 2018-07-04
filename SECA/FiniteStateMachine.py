# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Based on
#http://www.python-course.eu/finite_state_machine.php

"""
FiniteStateMachine Class
"""
class FiniteStateMachine:

	"""
	Method used to initialize a Finite State Machine (FSM)
	"""
	def __init__(self):
		self.__states = {}
		self.__startState = None
		self.__endStates = []
		self.__currentState = None
		self.__completed = False
		self.__startReady = True
		
	"""
	Adds a state the FSM
	"""
	def add_state(self, state):
		self.__states[state.getId()] = state
		if state.isStartState():
			self.__startState = state.getId()
		if state.isEndState():
			self.__endStates.append(state.getId())
			
	"""
	Sets the current state of the FSM
	"""
	def set_current(self, stateID):
		self.__currentState = stateID
		
	"""
	Returns the current state of the FSM
	""" 
	def get_current(self):
		return self.__currentState
		
	"""
	Returns the ID of the current state or inner (if exists)
	"""
	def get_innerStateID(self):
		state = self.__states[self.__currentState]
		if state.getInnerCModel()!=None:
			return state.getInnerCModel().getInnerStateID()
		else:
			return self.__currentState
			
	"""
	Returns the ID of the inner Conversational Model (if exists)
	"""
	def get_innerCModelID(self):
		if self.__currentState !=None:
			model = self.__states[self.__currentState].getInnerCModel()
			if model!=None:
				key = model.getInnerCModelID()
				if key!= None:
					return key
		return None
		
	"""
	Returns the keywords of all inner CM
	"""      
	def get_innerKeywords(self):
		keywords = []
		for state in self.__states.values():
			if state.getInnerCModel()!=None:
				keys = state.getInnerCModel().getAllInnerKeyWords()
				for key in keys:
					keywords.append(key)
		return keywords
		
	"""
	Returns the name of the inner CM with matching keywords
	"""  
	def check_innerCModelID(self, word):
		for state in self.__states.values():
			if state.getInnerCModel()!=None:
				key = state.getInnerCModel().checkInnerCModelID(word)
				if key!= None:
					return key
		return None
		
	"""
	Returns true if the FSM is completed
	""" 
	def isCompleted(self):
		return self.__completed
		
	"""
	Restarts the FSM
	""" 
	def restart(self):
		if self.__currentState != None:
			state = self.__states[self.__currentState]
			sub = state.getInnerCModel()
			if sub!=None:
				sub.restart()
		self.__currentState = self.__startState
		self.__completed = False
		self.__startReady = True
		
	"""
	Runs the FSM and updates its current state
	""" 
	def run(self, params = None):
		state = self.__states[self.__currentState]
		keys = None
		
		if self.__startReady:
			self.__startReady = False
			keys = state.onEntry(params)
			
		if keys==None:
			keys = state.onExit(params)
			
			newStateId = state.getNextState()
			newState = self.__states[newStateId]
			
			keysB = newState.onEntry(params)
			if keys==None:
				keys = keysB
			else:
				if keysB!=None:
					for key in keysB:
						keys.append(key)
						
			if newState.getId() in self.__endStates:
				self.__completed = True
			self.__currentState = newState.getId()
			
		return keys

"""
State Class
"""
class State(object):

	"""
	Method used to initialize a State
	"""
	def __init__(self, id, start=False, end=False, cModel=None):
		self.__id = id
		self.__isStart = start
		self.__isEnd = end
		self.__nextState = None
		self.__innerCModel = cModel
		
	"""
	Returns the id
	"""
	def getId(self):
		return self.__id
		
	"""
	Returns true if it is a start state
	"""  
	def isStartState(self):
		return self.__isStart
		
	"""
	Returns true if it is an end state
	"""
	def isEndState(self):
		return self.__isEnd
		
	"""
	Sets the next state
	"""
	def setNextState(self, stateID):
		self.__nextState = stateID
		
	"""
	Returns the name of the next state
	"""
	def getNextState(self):
		return self.__nextState
		
	"""
	Returns the innerCModel
	"""
	def getInnerCModel(self):
		return self.__innerCModel
		
	"""
	Method executed when the state is entered
	"""
	def OnEntry(self, params = None):
		""" An optional behavior that is executed when entered """
		return None
		
	"""
	Method executed when the state is exited
	"""
	def OnExit(self, params = None):
		""" An optional behavior executed whenever this state is exited """
		return None
