# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 11:12:01 2023

@author: rolfe
"""

from interfaces import IObserver_Control_generic_Note
from interfaces import IObserver_Control_generic_CC

from globalvars import Globals
from midicom import MidiComm
from typing import List  # I hope List is useable for standard Arrays


class Controls:

    __doc__ = """ this is the __doc__ string """

    def printall(Object):
        print("\n -- chords class structure, chords that can be invoked if  assigned to a midi message: ")
        i = 0
        for property, value in (vars(Object).items()):
            if not property.startswith('__'):
                if not property.startswith('printall'):
                    i = i+1
                    print("{}\t {} ".format(i, property.ljust(15)))

        print('\n')

################################################################################
    class sendChord_Note(IObserver_Control_generic_Note):
        '''
        0. Listen to the correct note
        1. place the incoming chord in the global register 
        2. play chord from global register
        '''
        _globals = Globals
        playchord = _globals.playChord # callback function

        # set typehints
        def __init__(self, cc_note: List[int], chord, midi: MidiComm):
            super().__init__(cc_note)
            self._chord = chord
            self._midi = midi

        def name(self) -> str:  # override function in parent-class
            ''' 
            The name also list eventually alternation chords 
            '''
            n = '*'
            if self._chord.alternations[0] is not None:
                n = self._chord.alternations[0].name

            return self.__class__.__name__ + " - " + self._chord.name + "\t -> " + n


        def execute(self, trigtype, message, args=None) -> None:

            print("hello from sendChord_Note ", self._cc_note)
            print("chord: ", self._chord.name)

            # 1. get triggered
            if trigtype == 'note_on':

                # 2. place chord's note array in globals ,  chord_current = []

                self._globals.chord_current = self._chord.index

            # 3. play chord from globals
                self._globals.playChord(self._midi)

            if trigtype == 'note_off':
                pass


        def _execute(self, trigtype, message, args=None):
            if message.type in self._triggers:
                if self._cc_note == message.note:
                    self.execute(trigtype, message, args)

##############################################################################


    class freezeroot_CC(IObserver_Control_generic_CC):

        _globals = Globals

        def __init__(self, cc_note: List[int], midi: MidiComm):  # wrong hints
            super().__init__(cc_note)
            self._midi = midi
            
        def name(self): return self.__class__.__name__ 

        def execute(self, trigmsgtype, mess, args=None):
        
            if mess.value > 64:
                return  # filter as hardware produce small ghost CC values

            #Globals, msgtype, note_cc, mess, midi = args
            #  if mess.value > 0 and mess.value < 127: return
            
            if mess.value < 64:
                return
            

            print("hello from freezeroot_CC ", self._cc_note)
            print("cc value: ", mess.value)
            

        def _execute(self, trigtype, message, args=None):
            if message.type in self._triggers:
                if self._cc_note == message.control:
                    self.execute(trigtype, message, args)


##############################################################################


    class alternateChord_CC(IObserver_Control_generic_CC):

        _globals = Globals

        def __init__(self, cc_note: List[int], midi: MidiComm):  # wrong hints
            super().__init__(cc_note)
            self._midi = midi
            
            
        def name(self): return self.__class__.__name__  

        def _playchord(self):
            self._midi.playChord(self._globals.chord_current,
                                 self._globals._global_chord_root)

        def execute(self, trigmsgtype, mess, args):  # called by _execute
            if mess.value < 127:
                return  # filter as hardware produce small ghost CC values

            # 1. retrieve current chord in globals
            # 2. ask the current chord for its alternative
            # 3. change current chord

            globchord = __class__._globals.chord_current  # also use self

            alt = globchord.alternations  # make abstract class for chords ?

            print("alternations: ", alt)

            try:
                newchord = alt[0]     # pick the first location for now

            except IndexError:
                print("Error - alternateChord_CC - execute - IndexError")

            globchord = newchord  # global reference with new alternate chord

            self._playchord()

            print("*** TRIGGERED ***")
            print("hello from alternateChord_CC ", self._cc_note)

        def _execute(self, trigtype, message, args=None):
            if message.type in self._triggers:
                if self._cc_note == [message.control]:
                    self.execute(trigtype, message, args)


# ##############################################################################


#     class chordInversions_CC(IObserver_Control_generic_CC):

#         _globals = Globals

#         def __init__(self, cc_note: List[int], midi: MidiComm):  # wrong hints
#             super().__init__()
#             self._cc_note = cc_note
#             self._midi = midi

#         def execute(self, trigmsgtype, mess, args):  # called by _execute
#             if mess.value < 127:
#                 return  # filter as hardware produce small ghost CC values

#             print("*** TRIGGERED ***")
#             print("hello from chordInversions_CC ", self._cc_note)
#             print("chord: ", self._chord.name)
#             print("cc value: ", mess.value)

#         def _execute(self, trigtype, message, args=None):
#             if message.type in self._triggers:
#                 if self._cc_note == [message.control]:
#                     self.execute(trigtype, message, args)


################################################################################

    # class sustain_trig_a_control_CC(IObserver_Sustain):
    #     '''
    #     1. listen to CC = 64 messages, and their values 

    #     2. trig a callback function

    #     3. callback triggers a control which is registered at instansiation

    #     '''
    #     _globals = Globals

    #     def __init__(self, midi: MidiComm):  # set typehints
    #         super().__init__()
    #         self._midi = midi

    #     def name(self) -> str:  # override function in parent-class
    #         return self.__class__.__name__

    #     def attachOutputCallback(self, callbackControl): 

    #         pass



    #     def execute(self, trigtype, message, args=None) -> None:

    #         print("hello from trig_a_control_1: ", self._cc_note)
    #         print("trigtype: ", trigtype)
    #         print("message: ", message)

    #         if message.value > 64:  # sustain pedal down, we got a CC
    #             print("message.value > 64")  # callbackControl(param)
    #             pass

    #         if message.value < 64:  # we got a CC
    #             pass

    #     def _execute(self, trigtype, message, args=None):
    #         if message.type in self._triggers:
    #             if self._cc_note == [message.control]:  # _cc_note = 64 in baseclass
    #                 self.execute(trigtype, message, args)

    #                 # _triggerValue = 64

################################################################################

    class trig_Control_generic_CC(IObserver_Control_generic_CC):
        '''
        used for register triggering  midi controls on my devices 
        
        
        '''
        _globals = Globals
        

        def __init__(self, cc_note, midi: MidiComm, callback = None):  # set typehints
            super().__init__(cc_note)
            self._midi = midi
            self._callback = callback


        def name(self) -> str:  # override function in parent-class
            return self.__class__.__name__



        def execute(self, trigtype, message, args=None) -> None:
            #print("\x1b[2J")
            cb=self._callback 

            # print("hello from trig_a_control_: ", self._cc_note)
            # print("trigtype: ", trigtype)
            # print("message.value: ", message.value)
            
            if cb is not None: 
                # testing out the a callback , but unsure about the overall structure 
                cb(message, self)
                pass
            
            # want to evoke the freeze controller in some way 
            
            
        def _execute(self, trigtype, message, args=None):
            if message.type in self._triggers:                
                if self._cc_note == message.control:  
                    self.execute(trigtype, message, args)

