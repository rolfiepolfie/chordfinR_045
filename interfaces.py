# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 21:37:29 2023

@author: rolfe
"""

from abc import ABC, abstractmethod

class IObserver_PC(ABC):
    
    def __init__(self):        
        self._triggers = ['program_change']
        self._PC = 0
    
    @abstractmethod    
    def name(self): pass  

    @abstractmethod
    def _execute(self, trigtype, message, args): pass

    @abstractmethod  
    def execute(self, trigtype, message, args): pass    
    
############################################################################
class IObserver_Sustain(ABC):
    
    def __init__(self):
        self._triggers = ['control_change']
        self._cc_note = 64
        
    @abstractmethod          
    def name(self): pass 
    
    @abstractmethod
    def _execute(self, trigtype, message, args): pass
        
    @abstractmethod
    def execute(self, trigtype, message, args): pass

############################################################################
class IObserver_Control_generic_CC(ABC): #make these more generic and _cc_note in constructor
    
    def __init__(self, cc_note):
        self._triggers = ['control_change']
        self._cc_note = cc_note
    
    @abstractmethod         
    def name(self): pass 
        
    @abstractmethod
    def _execute(self, trigtype, message, args): pass
    
    @abstractmethod
    def execute(self, trigtype, message, args): pass  

  
############################################################################
class IObserver_Control_generic_Note(ABC): #make these more generic and _cc_note in constructor
    
    def __init__(self, cc_note):
        self._triggers = ['note_on', 'note_off']
        self._cc_note = cc_note
    
    @abstractmethod         
    def name(self): pass 
        
    @abstractmethod
    def _execute(self, trigtype, message, args): pass
        
    @abstractmethod
    def execute(self, trigtype, message, args): pass  
  
  