# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 23:03:37 2023

@author: test
"""

class UserInteraction:
    
    def askuseropenports(rv, midi, filt, ports):
        
        
        print("open inport for bass: ")
        #if ans == 'y':
        ports.openInport_bass(rv.in_index_bass) 
        midi.setinPort_bass(ports._inPort_bass, ports._inPort_bass_name, filt.trigBass) 
        time.sleep(0.5)
                        
        ports.openInport_control(rv.in_index_control1) 
        midi.setinPort_controlButtons(ports._inPort_control, ports._inPort_control_name, filt.trigControlChord) 
        time.sleep(0.5)
        
        print("open inport for control2: ")
        
        if rv.in_index_control2 != -1: 
        
            ports.openInport_control(rv.in_index_control2) 
            midi.setinPort_controlButtons(ports._inPort_control, ports._inPort_control_name, filt.trigControlChord) 
        
        else:
            print("NB ** port not opened **")
                    
        
        time.sleep(0.5)


    def readportnumbers():
        
        @dataclass
        class Returnvalue:
            out_index:          int
            in_index_bass:      int
            in_index_control1:  int
            in_index_control2:  int
            
        while True: # read in a midi port device 
            try:
                print(" *********** -1 if this service is not wanted. ************* ")
                print(" - ")
                out_index = int(input("For chord output, enter a number (default 0): ") or "0")
                print('\n')
                
                in_index_bass = int(input("For bass input, enter a number(default 0): ") or "0") #1
                      
                in_index_control1 = int(input("For control input1, enter a number(default 1): ") or "1") #3
                in_index_control2 = int(input("For control input2, enter a number(default -1): ") or "-1") #0
                
                break
            
            except Exception as e:
                print("er, ror: " + str(e))
                
        return Returnvalue(out_index, in_index_bass, in_index_control1, in_index_control2)