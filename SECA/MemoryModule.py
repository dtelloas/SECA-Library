# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
SECA Memory Module Class
"""
class MemoryModule(object):

	"""
	Method used to initialize the Memory Module
	"""
	def __init__(self):
		self.__memories = {} 
			#Keys of the dictionary (memoryId)
			#Content (Memory object)
		self.__lastSaid = {} #Can be used for completing information
			#Keys of the dictionary (classes)
			#Content (memoryId)
			
	"""
	Adds a certain memory to the Memory Module
	"""	        
	def addMemory(self,id,cl):
		if id not in self.__memories.keys():
			self.__memories[id] = Memory(id,cl)
			if cl not in self.__lastSaid.keys():
				self.__lastSaid[cl]=""
				
	"""
	Updated the counter of a certain memory
	"""	
	def updateMemory(self, id):
		if id in self.__memories.keys():
			self.__memories[id].updateNOcc()
			self.__lastSaid[self.__memories[id].getClass()] = id
			
	"""
	Returns the id of the last said memory of a certain class
	"""		    
	def getLastSaid(self, cl):
		return self.__lastSaid[cl]
		
	"""
	Returns a list with the less said memoris of a certain class excluding the last said one
	"""
	def getLessSaid(self, list):
		lessFreq = float("inf")
		lessList = []
		for mem in list:
			if mem in self.__memories.keys():
				if self.__memories[mem].getNOcc() == lessFreq:
					lessList.append(mem)
				elif self.__memories[mem].getNOcc() < lessFreq:
					lessList = []
					lessList.append(mem)
					lessFreq = self.__memories[mem].getNOcc()
			else:
				lessList.append(mem)
				lessFreq = 0
		if len(lessList)>1:
			remM = self.getLastSaid(self.__memories[lessList[0]].getClass())
			if remM in lessList:
				lessList.remove(remM)
		return lessList
	
	"""
	Returns the counter of a memory
	"""	    
	def getCounter(self,id):
		return self.__memories[id].getNOcc()
		
	"""
	Returns the class of a memory
	"""	
	def getClass(self,id):
		return self.__memories[id].getClass()
		
	"""
	Loads the status of the Memory Module
	"""	
	def loadMemory(self, ids, values, classes):
		for i in range (len(ids)):
			self.__memories[ids[i]] = Memory(ids[i],classes[i],values[i])
    		
"""
Memory Class
"""
class Memory(object):

	"""
	Method used to initialize a Memory
	"""
	def __init__(self, id, cl, nOcc=0):
		self.__id = id
		self.__nOcc = nOcc
		self.__class = cl
	
	"""
	Returns the memory Id
	"""	
	def getId(self):
		return self.__id
	
	"""
	Returns the number of occurrences of the memory
	"""	
	def getNOcc(self):
		return self.__nOcc
	
	"""
	Updates the number of occurrences of the memory
	"""	
	def updateNOcc(self):
		self.__nOcc+=1
	
	"""
	Returns the class of the memory
	"""	
	def getClass(self):
		return self.__class