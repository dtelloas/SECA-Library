# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ConversationalModule import *
from KnowledgeModule import *
from MemoryModule import *
from PersonalityModule import *
from NeedsModule import *
from EmpathyModule import *
from NLPModule import *

import unidecode
import string


"""
SECA Controller Class
"""
class SECA(object):
    
    """
    Method used to initialize the SECA
    """
    def __init__(self, agentID, initialMood, initialEmotion, moodMatrix, emotionMatrix, meprobMatrix, NLPMod):
    
    	#Seca ID
    	self.__ID = agentID
    	
    	#Conversational Module initialization
        self.__conversationalMod = ConversationalModule()
        
        #Knowledge Module initialization
        self.__knowledgeMod = KnowledgeModule()
        
        #Memory Module initialization
        self.__memoryMod = MemoryModule()
        
        #Personality Module initialization
        self.__personalityMod = PersonalityModule(initialMood, initialEmotion, moodMatrix, emotionMatrix, meprobMatrix)
        
        #Needs Module initialization
        self.__needsMod = NeedsModule()
        
        #Empathy Module initialization
        self.__empathyMod = EmpathyModule()
        
        #NLP Module initialization
        self.__nlpMod = NLPMod
    
    """
    Method that returns the ID of the agent
    """
    def getID(self):
    	return self.__ID
    
    
    #
    # CONVERSATIONAL MODULE RELATED FUNCTIONS
    #
    """
    Adds a conversation to the Conversational Module of the agent
    """
    def addConversation (self, conv):
    	self.__conversationalMod.addConversation(conv)
    
    """
    Updates the Conversational Module
    """
    def updateConvMod (self, convID, params = None):
    	return self.__conversationalMod.update(convID, params)
    
    """
    Cancels the current conversation of the Conversational Module
    """
    def cancelConversation (self):
    	self.__conversationalMod.cancel()
    
    """
    Returns the ID of the current inner Dialog
    """
    def getInnerDialogID(self):
    	return self.__conversationalMod.getInnerDialogID()
    	
    """
    Returns the ID of the current inner State
    """
    def getInnerStateID (self):
    	return self.__conversationalMod.getInnerStateID()
    	

    #
    # KNOWLEDGE MODULE RELATED FUNCTIONS
    #
    """
    Adds AIML file to the Knowledge Module
    """
    def addAIML(self, aimlFile):
    	self.__knowledgeMod.loadAIML(aimlFile)
    
    """
    Returns AIML corresponding to the message parameter
    """
    def getAIML (self, message):
        return self.__knowledgeMod.getAIML(message)
    
    """
    Adds certain Knowledge to the Knowledge Module
    """
    def addKnowledge (self, know):
    	self.__knowledgeMod.addKnowledge(know)
    
    """
    Returns the less said knowledge concept associated to a certain topic
    """	
    def getLessSaid(self,topic):
    	knowL = self.__knowledgeMod.getKnowledgeList(topic)
    	if knowL!=None:
    		lessSaidList = self.__memoryMod.getLessSaid(knowL)
    		key = random.choice(lessSaidList)
    		return key
    	else:
    		return key
    
    """
    Returns all concepts in the Knowledge Module
    """		
    def getKnowledgeConcepts(self):
    	return self.__knowledgeMod.getAllKnowledgeConcepts()
    
    """
    Returns a random concept from a certain topic
    """	
    def getKnowledgeConcept(self,topic):
    	knowL = self.__knowledgeMod.getKnowledgeList(topic)
    	if knowL!=None:
    		lessSaidList = self.__memoryMod.getLessSaid(knowL)
    		key = random.choice(lessSaidList)
    		return key
    	else:
    		return key
    
    """
    Returns the identified concepts of a certain topic in words and None if nothing is found
    """	
    def checkKnown(self, topic, words):
    	wordsS = ""
    	for word in words:
    		wordsS+=word+" "
    	knowL = self.__knowledgeMod.getKnowledgeList(topic)
    	knowLclean = []
    	for word in knowL:
    		word = unidecode.unidecode(word)
    		wordL = word.split("_")
    		knowLclean.append(wordL)
    	match = []
    	for list in knowLclean:
    		for word in words:
    			if word in list:
    				match.append(list)
    	if len(match)>0:
    		maxElem = 0
    		maxCount = 0
    		for list in knowLclean:
    			newCount = match.count(list)
    			if newCount>maxCount:
    				maxCount = newCount
    				maxElem = list
    		if unidecode.unidecode(knowL[knowLclean.index(maxElem)].replace("_"," ")) in wordsS:
    			return knowL[knowLclean.index(maxElem)]
    		else:
    			return None
    	return None
    
    
    #
    # MEMORY MODULE RELATED FUNCTIONS
    #
    """
    Returns the Memory Module
    """	
    def getMemory(self):
    	return self.__memoryMod
    
    """
    Adds a certain memory to the Memory Module
    """	
    def addMemory(self,id,cl):
    	self.__memoryMod.addMemory(id,cl)
    
    """
    Updated the counter of a certain memory
    """	
    def updateMemory (self, id):
    	self.__memoryMod.updateMemory(id)
    
    """
    Returns the id of the last said memory of a certain class
    """		
    def getLastSaid(self,cl):
    	return self.__memoryMod.getLastSaid(cl)
    
    
    #
    # PERSONALITY MODULE RELATED FUNCTIONS
    #
    """
    Returns the current mood of the agent
    """	
    def getCurrMood (self):
        return self.__personalityMod.getMood()
    
    """
    Returns the current emotion of the agent
    """	
    def getCurrEmotion (self):
        return self.__personalityMod.getEmotion()
    
    """
    Sets the current mood of the agent
    """	
    def setCurrMood(self, cMood):
    	self.__personalityMod.setMood(cMood)
    	
    """
    Sets the current emotion of the agent
    """	
    def setCurrEmotion(self, cEmotion):
    	self.__personalityMod.setEmotion(cEmotion)
    
    
    #
    # NEEDS MODULE RELATED FUNCTIONS
    #
    """
    Adds a need to the Needs Module of the agent
    """	
    def addNeed(self,label,t):
    	self.__needsMod.addNeed(label,t)
    	
    """
    Returns true if a certain need is active
    """	
    def checkNeed (self, label):
    	return self.__needsMod.checkNeed(label)
    	
    """
    Restarts the timer of a certain need
    """	
    def restartNeed (self, label):
    	self.__needsMod.restartNeed(label)
    
    	
    #
    # EMPATHY MODULE RELATED FUNCTIONS
    #
    """
    Returns the Empathy Module
    """	
    def getEmpathy(self):
    	return self.__empathyMod
    
    """
    Adds an empathy component to the Empathy Module
    """	
    def addEmpathyComponent(self, label, initialValue, minV, maxV):
    	self.__empathyMod.addComponent(label, initialValue, minV, maxV)
    
    """
    Updates an empathy component with a certain change
    """	
    def updateEmpathyComponent(self, label, change):
    	self.__empathyMod.updateComponent(label, change)
    	
    """
    Updates the maximum value of a certain empathy component
    """	
    def updateEmpathyComponentMax(self, label, change):
    	self.__empathyMod.updateMaxValue(label, change)
    
    """
    Resets an empathy component to its minimum value
    """	
    def resetEmpathyComponentValue(self, label):
    	self.__empathyMod.resetValue(label)
    
    """
    Returns the current value of an empathy component
    """	
    def checkEmpathyComponentValue(self, label):
    	return self.__empathyMod.checkComponentValue(label)
    
    """
    Returns the current max value of an empathy component
    """	
    def checkEmpathyComponentMaxValue(self, label):
    	return self.__empathyMod.checkComponentMaxValue(label)
    
    """
    Returns true if an empaty component value equals to its current max value
    """	
    def checkEmpathyComponentIsMax(self, label):
    	return self.__empathyMod.compValIsMax(label)
    	
    	
    #
    # NLP MODULE RELATED FUNCTIONS
    #
    """
    Returns a list with preprocessed words of a certain text (1) and its embedding(0)
    """	
    def preprocess(self,text):
    	return self.__nlpMod.preprocessing(text) #0 is features 1 is words
    
    """
    Returns the classification result of a certain type of a message
    """	
    def classify(self,type,words,feat,message):
    	return self.__nlpMod.classification(type,words,feat,message)

    
    #
    # FUNCTION TO UPDATE THE SECA
    #
    """
    Method used to get the answer of a message given a conversation and some optional parameters
    """
    def getAnswer(self,message, conversation, parameters):
    	"""
    	To be overwritten
    	"""
    	return None
    
    """
    Function that given certain keys, updated the state of the SECA
    Returns a message that is going to be delivered to the user
    """	
    def update (self, keys):
    	answer = "";
    	for key in keys:
    		aimlInfo = self.getAIML(key)
    		#Response is parsed
    		parsedMessage = self.parserAIML(aimlInfo)
    		if keys.index(key)==0:
    			self.__personalityMod.update(parsedMessage[0])
    		answer += parsedMessage[1][self.__personalityMod.getEmotion()]
    		answer += ";"
    	self.saveState()
    	return answer[:len(answer)-1]
    	
    """
    Returns the information obtained from the aiml module parsed
    """
    def parserAIML(self,message):
    	v = []
    	aux = ""
    	mSplit = message.split(" ",1)
    	
    	for i in range(1,len(mSplit[0])):
    		if mSplit[0][i] == ',' or mSplit[0][i] == ']':
    			v.append(float(aux))
    			aux = ""
    		else:
    			aux += mSplit[0][i]
    			
    	mSplit2 = mSplit[1].split("% ")
    	mSplit2[len(mSplit2)-1] = mSplit2[len(mSplit2)-1][:len(mSplit2[len(mSplit2)-1])-1]
    	return [v, mSplit2]
    
    """
    Performs a basic cleaning
    """
    def cleanKey(self,key):
    	key = unicode(key)
    	key = unidecode.unidecode(key)
    	for p in string.punctuation:
    		key = key.replace(p,"")
    	key = key.upper()
    	return key

        
    #
    # DATA STORAGE RELATED FUNCTIONS
    # MUST BE OVERWRITTEN DEPENDING ON THE SAVING PLACE AND CONDITIONS
    #
    """
    Saves the status of a memory
    """
    def saveMemory(self, id):
        """
        To be overwritten
        """
        return None
    
    """
    Loads the status of the Memory Module
    """
    def loadMemory(self, ids, values):
        """
        To be overwritten
        """
    	return None

	"""
    Saves the personality state of the agent
    """
    def saveState(self):
        """
        To be overwritten
        """
    	return None
    
    """
    Loads the personality state of the agent
    """
    def loadState(self,mood,emotion):
    	"""
    	To be overwritten
    	"""
    	return None
    
    """
    Saves the status of an empathy component
    """    
    def saveEmpathyStatus(self, component):
        """
        To be overwritten
        """
        return None
    
    """
    Loads the status of the Empathy Module
    """ 
    def loadEmpathyStatus(self, labels, values):
        """
        To be overwritten
        """
    	return None
