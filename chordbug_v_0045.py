# -*- coding: utf-8 -*- 

import logging as logg
import config ##globals config variables for this app 

from ports import Ports
from chords import Chords
from midicom import MidiComm
from controls import Controls
from midiMessage import Midimess
from utilities import Misc
from filterMidi import Filter 

from sessionclass import SessionMain
from sessionclass import UserInteraction as ui # set this in a proper system

import rtmidi as rt
import sys
import mido

from globalvars import Globals
from paletteSelector import Palettes, PaletteSelector
import winsound
from timeit import default_timer as timer

## TEST
### testing callback which is registered with any controller of choice 
## used for controls that shall evoke other controls
## a control must be registered with this callback
def callback_controls_live(msg, instance):   
    print('callback_controls_live: ', msg)
    
    print("\x1b[2J")
    
    start = timer()
    if instance.name() == 'trig_Control_generic_CC':
       
        if instance._cc_note == 5:
            print('*hello - trig_Control_generic_CC 5')
        
            arrPalette = paletteselector.scan(msg.value)
            session.registerControls(arrPalette) 
            session.showControlsRegistered(Globals.controls) 
        
        if instance._cc_note == 6:
            print('*hello - trig_Control_generic_CC 6')
            
    end = timer()
    print("callback_controls_live: ", end - start)      

#being called when the foot controller hardware is invoked                   
def callback_Control_Buttons(msg) -> None:
    
    Globals.scanControls(msg)

    
def callbackBass(msg) -> None:  #rename msg to midiOriginal    
    ''' 
    msg = original MIDI message, recall only original messages for the engine 
        set flag global_bassdown
    set root-note in global_chord_root
    send bass-note as midi-trough if requested 
    '''
    midimsg = Midimess(msg) # in future, return a mido.message(..) as they can be sent as regular midi messages
    #midimsg = Midimess(msg).mido <-future, and use midimsg only
    Globals.scanControls(msg) #scancontrols can make use of the midimsg to save time 
    
    
    def alterOutMidiChannel(newchannel):
        '''
        if you want alter the output midichannel only
        while retaining  other parameters  like another channel'''
        midi.sendMessageOut(msg.copy(channel=newchannel))
        
    if session._midiTrough:       
        midi.sendMessageOut(msg) 
        # mimics the same as midi-through 
        # need original midi message!
        # alterOutMidiChannel(10)
    
    if midimsg.isnoteOn():
        Globals.global_bassdown=True
        
        if Globals.global_Control_disable_chord_root == False: #control = freeze-root
           Globals.global_chord_root = msg.note #we know it is a note at this stage
            
        #print("global_chord_root note: ", glob.Globals.global_chord_root)
        return
        
    if midimsg.isnoteOff():
        Globals.global_bassdown=False
        #print("Globals.global_bassdown=False")
        return
        

def setupSession(session : SessionMain , midi, ports, filterMidi, glob : Globals, callbackLive) -> None:
    
    palettes = Palettes(Controls, Chords, midi, callbackLive)

    normal1 = palettes.palette_normal1()
    normal2 = palettes.palette_normal2()
    blues = palettes.Palette_blues1()
    
    global paletteselector  # just for test
         
    paletteselector = PaletteSelector(normal1, normal2, blues)   ### NB ; SET TO:     Global.controls
    session.registerControls(normal1)   # loads global control array with controls 
    
    # remark Misc class object not an instance, test globals
    Controls.printall(Controls) #to be improved 
      
    session.showControlsRegistered(Globals.controls) 
    
    # midichannels [0...15] - other subclasses copy these values 
    session.midichannelBass=3
    session.midiChannelControls=0
    session.midiChannelOut=15  
    session._midiTrough = True   
        
    # attach big objects
    session.filterMidi = filterMidi
    session.midi = midi
    session.ports = ports
    
    session.reportDevices() #port devices
    portindexes=ui.readportnumbers()  # reads port indexes from user
        
    session.setupSession(portindexes)

    session.testout(60)
    session.report()


def _destruct():
    '''
    This will work as the destructor in the later Session Class 
    '''        
    if midi.InportsEmty()== False:
        print('* sending all notes off')
        midi.sendAllNotesOff() #hardware dependent 

        print('* closing all ports')
        ports.closeAllPorts() 
        
    ports.report()
    print('* PROGRAM ENDED *')
    Misc.printTitle(mido, rt, sys, config.___version___, config.___title___)
    winsound.Beep(int(200), 800)
    raise SystemExit(0) #clean way to exit , no traceback



# Global instances to be shared among modules 
# testing out the palette (cordpalette selector)

session     = SessionMain()
midi        = MidiComm(mido, offset=config.__offset__, chordTimeLength=config.__chordTimeLength__) #offset = transpose 
ports       = Ports(mido)
filterMidi  = Filter(callbackBass, callback_Control_Buttons) 

## new idea
#
# use the sustain pedal to "lock" the chord?
# we also need a C_plus or C-aug = C-augmented (sharpen 5th command)
# an add6, add2 to 7 = 9th chord?   also dim
# function for going to the most used chord - reset-chord ... minor, major
#




def main():
    #logg.basicConfig(level=logg.INFO)
    
    #https://www.pylenin.com/blogs/python-logging-guide/
    logg.basicConfig(stream=sys.stdout, level=logg.INFO)
    # logg.debug('debug')
    logg.info("info message 123")
    # logg.warning('warning')
    # logg.error('error')
    Misc.printLogo()
    Misc.printTitle(mido, rt, sys, config.___version___, config.___title___)
    setupSession(session, midi, ports, filterMidi, Globals, callback_controls_live) 
    Misc.printMainMenu()

    midi.startLoop_keyboardlistener(_destruct, midi, Misc, session) # polling the keyboard 
        
##################################################################################   
if __name__ == "__main__": main()    
    
    