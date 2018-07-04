# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
SECA Empathy Module Class
"""
class EmpathyModule(object):

	"""
	Method used to initialize the Empathy Module
	"""
	def __init__(self):
		self.__empathyComponents = {}
	
	"""
	Adds an empathy component to the Empathy Module
	"""	
	def addComponent(self, label, initialValue = 50, minV=0, maxV=100):
		self.__empathyComponents[label] = EmpathyComponent(label,initialValue,minV,maxV)

	"""
	Updates an empathy component with a certain change
	"""	
	def updateComponent(self, label, change):
		self.__empathyComponents[label].updateVal(change)

	"""
    Updates the maximum value of a certain empathy component
    """	
	def updateMaxValue(self,label,change):
		self.__empathyComponents[label].updateMaxVal(change)
		
	"""
    Resets an empathy component to its minimum value
    """	
	def resetValue(self,label):
		self.__empathyComponents[label].resetValue()

	"""
	Returns the current value of an empathy component
	""" 
	def checkComponentValue(self, label):
		return self.__empathyComponents[label].getValue()
	
	"""
	Returns the current max value of an empathy component
	"""	    
	def checkComponentMaxValue(self, label):
		return self.__empathyComponents[label].getMaxValue()
	
	"""
    Returns true if an empaty component value equals to its current max value
    """	
	def compValIsMax(self,label):
		return self.__empathyComponents[label].valIsMax()
	
	"""
    Loads the status of the Empathy Module
    """ 
	def loadEmpathyStatus(self, labels, values, maxValues):
		for i in range (len(labels)):
			if labels[i] in self.__empathyComponents.keys():
				self.__empathyComponents[labels[i]].setValue(values[i])
				self.__empathyComponents[labels[i]].setMaxValue(maxValues[i])

"""
Empathy Component Class
"""           
class EmpathyComponent(object):

	"""
	Method used to initialize an Empathy Component
	"""
	def __init__(self, label, initialV, minV, maxV):
		self.__label = label
		self.__value = initialV
		self.__minVal = minV
		self.__maxVal = maxV
		self.__currMaxVal = maxV
		
	"""
	Returns the label of the component
	"""
	def getLabel(self):
		return self.__label
		
	"""
	Returns the current value of the component
	"""
	def getValue(self):
		return self.__value
		
	"""
	Returns the current maxValue of the component
	"""
	def getMaxValue(self):
		return self.__currMaxVal
		
	"""
	Sets the value of the component
	"""
	def setValue(self, newVal):
		self.__value = newVal
		
	"""
	Sets the current maxValue of the component
	"""
	def setMaxValue(self, newVal):
		if newVal>self.__maxVal:
			self.__currMaxVal = newVal
			
	"""
	Updates the value of the component through a certain change
	"""
	def updateVal(self, change):
		self.__value +=change
		if self.__value<self.__minVal:
			self.__value = self.__minVal
		elif self.__value >self.__currMaxVal:
			self.__value = self.__currMaxVal
			
	"""
	Updates the current maxVal of the component through a certain change
	"""
	def updateMaxVal(self, change):
		self.__currMaxVal +=change
		if self.__currMaxVal<self.__maxVal:
			self.__currMaxVal = self.__maxVal
			
	"""
	Returns true if the current value of the component equals its current maxValue
	"""
	def valIsMax(self):
		if self.__value==self.__currMaxVal:
			return True
		else:
			return False
		
	"""
	Sets the value of the component to its minValue
	"""    
	def resetValue(self):
		self.__value = self.__minVal