# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 15:51:41 2023

@author: rolfe
"""
from controls import Controls
from chords import Chords
from midicom import MidiComm
from collections.abc import Callable
class Palettes:
    
    def __init__(self, controls: Controls , chords : Chords, midi : MidiComm, callbackLive : Callable): 
        
        self._controls = controls
        self._chords = chords
        self._midi = midi
        self._callbackLive = callbackLive
        

    
    def palette_normal1(self):
        
        chords=self._chords
        controls=self._controls
        
        midi = self._midi 
        maj7 = chords.maj7
        maj7.alternations  = [None]
        
        major=chords.major
        major.alternations = [chords.cm7_plus_2]
        
        sus2 = chords.sus2
        sus2.alternations = [chords.sus4]
        
        sept7 = chords.normal_7th
        sept7.alternations = [chords.nine9] # or minor7
        
        minor = chords.minor
        minor.alternations = [chords.minor7]
        
        minor7 = chords.minor7
        minor7.alternations = [None]
        
        # chords
        send_maj7_note      = controls.sendChord_Note(12,     maj7,   midi)
        send_sept7_note     = controls.sendChord_Note(14,     sept7,  midi)
        send_major_note     = controls.sendChord_Note(16,     major,  midi)
        send_minor_note     = controls.sendChord_Note(17,     minor,  midi)
        send_sus2_note      = controls.sendChord_Note(19,     sus2,   midi)
        send_minor7_note    = controls.sendChord_Note(20,     minor7, midi)
        
        # controls
        alternate_cc = controls.alternateChord_CC(22, midi) #uses global chord reference
        freeze_cc = controls.freezeroot_CC(21,        midi)   
        
        trigControl5 = controls.trig_Control_generic_CC(5, midi, self._callbackLive) # a control knob on the bass device 

        
        
        c=[]
        c.append(send_maj7_note)
        c.append(send_sept7_note) 
        c.append(send_major_note) 
        c.append(send_minor_note) 
        c.append(send_sus2_note) 
        c.append(send_minor7_note) 
        c.append(alternate_cc) 
        c.append(freeze_cc) 
        c.append(trigControl5) 

        
        return c
        
    
    def palette_normal2(self):
        
        chords=self._chords
        controls=self._controls
        midi = self._midi 
        
        maj7 = chords.maj7
        maj7.alternations  = [None]
        
        major=chords.major
        major.alternations = [chords.cm7_plus_2]
        
        sus2 = chords.sus2
        sus2.alternations = [chords.sus4]
        
        sept7 = chords.normal_7th
        sept7.alternations = [chords.nine9] # or minor7
        
        minor = chords.minor
        minor.alternations = [chords.minor7]
        
        minor7 = chords.minor7
        minor7.alternations = [None]
        
        # chords
        send_maj7_note      = controls.sendChord_Note(12,     maj7,   midi)
        send_sept7_note     = controls.sendChord_Note(14,     sept7,  midi)
        send_major_note     = controls.sendChord_Note(16,     major,  midi)
        send_minor_note     = controls.sendChord_Note(17,     minor,  midi)
        send_sus2_note      = controls.sendChord_Note(19,     sus2,   midi)
        send_minor7_note    = controls.sendChord_Note(20,     minor7, midi)
        
        # controls
        alternate_cc = controls.alternateChord_CC(22, midi) #uses global chord reference
        freeze_cc = controls.freezeroot_CC(21,        midi)    
        
        trigControl5 = controls.trig_Control_generic_CC(5, midi, self._callbackLive) # a control knob on the bass device 
    

        
        c=[]
        c.append(send_maj7_note)
        c.append(send_sept7_note) 
        c.append(send_major_note) 
        c.append(send_minor_note) 
        c.append(send_sus2_note) 
        c.append(send_minor7_note) 
        c.append(alternate_cc) 
        c.append(freeze_cc) 
        c.append(trigControl5)

        
        return c

    def Palette_blues1(self):
        chords=self._chords
        controls=self._controls
        midi = self._midi 
        
        major9 = chords.nine9
        major9.alternations  = [None]
        
        major=chords.major
        major.alternations = [chords.cm7_plus_2]
        
        sus2 = chords.sus2
        sus2.alternations = [chords.sus4]
        
        sept7 = chords.normal_7th
        sept7.alternations = [chords.nine9] # or minor7
        
        minor = chords.minor
        minor.alternations = [chords.minor7]
        
        minor7 = chords.minor7
        minor7.alternations = [None]
        
        # chords
        send_major9_note    = controls.sendChord_Note(12,     major9, midi)
        send_sept7_note     = controls.sendChord_Note(14,     sept7,  midi)
        send_major_note     = controls.sendChord_Note(16,     major,  midi)
        send_minor_note     = controls.sendChord_Note(17,     minor,  midi)
        send_sus2_note      = controls.sendChord_Note(19,     sus2,   midi)
        send_minor7_note    = controls.sendChord_Note(20,     minor7, midi)
        
        # controls
        alternate_cc = controls.alternateChord_CC(22, midi) #uses global chord reference
        freeze_cc = controls.freezeroot_CC(21,        midi)    
        
    
        trigControl5 = controls.trig_Control_generic_CC(5, midi, self._callbackLive) # a control knob on the bass device 
        trigControl6 = controls.trig_Control_generic_CC(6, midi, self._callbackLive)


        
        c=[]
        c.append(send_major9_note)
        c.append(send_sept7_note) 
        c.append(send_major_note) 
        c.append(send_minor_note) 
        c.append(send_sus2_note) 
        c.append(send_minor7_note) 
        c.append(alternate_cc) 
        c.append(freeze_cc) 
        c.append(trigControl5)
        c.append(trigControl6)
        
        return c
        
        
         




class PaletteSelector():
    
    MAX_VALUE = 126
   
    def __init__(self, controls1 : list, controls2 : list, controls3 : list):
   
        self._arr1 = controls1 # array with controls that evoke chords  
        self._arr2 = controls2
        self._arr3 = controls3
       
        self._palette = self._arr1
       
       
    def palette(self): return self.actual
              
    def _control1(self):
        self._palette = self._arr1
   
    def _control2(self):
        self._palette = self._arr2
   
    def _control3(self):
        self._palette = self._arr3
      
    def scan(self, param : int): #param is some CC message from a callback message
   
        if param in range(0, 40):
            self._control1()
           
        if param in range(40, 80):
            self._control2()
       
        if param in range(80, __class__.MAX_VALUE):
           self. _control3()
                   
        return self._palette            
    
