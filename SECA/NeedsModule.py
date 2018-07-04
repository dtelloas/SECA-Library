# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from threading import Timer

"""
SECA Needs Module Class
"""
class NeedsModule(object):

	"""
	Method used to initialize the Needs Module
	"""
	def __init__(self):
		self.__needs = {} 
			#Keys of the dictionary (needLabel)
			#Content (Need object)
			
	"""
	Adds a need to the Needs Module
	"""	
	def addNeed(self,label,t):
		if label not in self.__needs.keys():
			self.__needs[label] = Need(label,t)
			
	"""
	Returns true if a certain need is active
	"""	
	def checkNeed(self, label):
		return self.__needs[label].checkNeed()
		
	"""
	Restarts the timer of a certain need
	"""	    
	def restartNeed(self, label):
		self.__needs[label].restartNeed()
        

"""
Need Class
"""
class Need(object):

	"""
	Method used to initialize a Need
	"""
	def __init__(self, label, t):
		self.__label = label
		self.__active = False #Need active (True) or not (False)
		self.__time = t
		self.__needT = None #Timer
		
	"""
	Returns the need label
	"""
	def getLabel(self):
		return self.__label
		
	"""
	Returns true if the need is active
	"""
	def checkNeed(self):
		return self.__active
		
	"""
	Activates the need
	"""    
	def needT(self):
		self.__active = True
		
	"""
	Restarts a need timer
	"""	
	def restartNeed(self):
		self.__active = False
		if self.__needT!=None:
			self.__needT.cancel()
		self.__needT = Timer(self.__time,self.needT)
		self.__needT.start()