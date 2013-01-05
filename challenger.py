#!/usr/bin/python3

#    Challenger
#     - Challenge a LUSAS licence server until a licence is gained.
#    Copyright (C) 2011 thomas michael wallace
#      < www.thomasmichaelwallace.co.uk >

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# imports

import re
import string
import time
import os
import sys
import subprocess
import msvcrt
import webbrowser

# configuration
LUSAS_VERSION = "147"
LSM_KEYID = 'LusasM_WXYZ'

# paths
LSM_LOCATION = """C:\LUSAS""" + LUSAS_VERSION + """\Programs\License\lsmon.exe"""
LUS_LOCATION = """C:\LUSAS""" + LUSAS_VERSION + """\Programs\lusas_m.exe"""

# timer
MEN_WAIT = 1
LSM_WAIT = 10
LUS_WAIT = 5

# common informaiton
CHALLENGER_VERSION = "2.5"

# key tokens
LSM_FEATURE = 'Feature name'
LSM_MAX_LICENCES = 'Maximum concurrent user(s)'
LSM_USED_LICENCES = 'Unreserved tokens in use'
LSM_USER = 'User name'

# ui options
BAR_OPEN = "["
BAR_ON = "."
BAR_OFF = " "
BAR_CLOSE = "]"
BAR_LENGTH = 10

# copyleft licence

print(
"""Challenger - Copyright (C) 2011 thomas michael wallace
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions."""
    )



class lsmon_py():
    """ Provides an interface between LUSAS licence monitor and Python. """

    def __init__(self):        
        self.refresh()
    
    def query_lsmon(self):
        """ Returns the LUSAS licence monitor status. """
        
        # start lusas licence monitor, send enter and fetch output
        lsmon = subprocess.Popen(
            LSM_LOCATION,    
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        stdout_value, stderr_value = lsmon.communicate('\r\n'.encode())

        # remove literal versions of special charectors
        buffer = str(stdout_value)
        buffer = buffer.replace('\\t','')
        buffer = buffer.replace('"','')
        
        return buffer.split('\\r\\n')
        
    def parse(self, option_string):
        """ Parses lsmon output into individual options. """
    
        options = re.findall(
            '[\s]*\|-[\s]*'         # initial whitespace, tree
            '([\w\d\s()]+)'         # variable name
            '[\s]*:[\s]*'           # sepeartor
            '([\w\d\s]+)'           # variable value
            '(\\t)*'                # white space
            ,option_string)
    
        if options:    
            return [options[0][0].strip(), options[0][1].strip()]
        else:
            return False
        
    def refresh(self):
        """ Requery and refersh interface information. """        

        # reset class state
        self.max_licences = 0
        self.used_licences = 0
        self.users = []        
        polling = False
        
        # re-query lusas licence monitor
        for response in self.query_lsmon():    
            option = self.parse(response)
    
            # set parsed input
            if not option:
                continue
            token = option[0]
            value = option[1]
                
            # ignore lines not within licence key feature
            if token == LSM_FEATURE:                
                if value == LSM_KEYID:
                    polling = True
                else:
                    polling = False

            if polling:
                # fetch licence counts
                if token == LSM_MAX_LICENCES:
                    self.max_licences = value                                
                elif token == LSM_USED_LICENCES:
                    self.used_licences = value
                
                # fetch current user list
                elif token == LSM_USER:
                    self.users.append(value)
        
        # check if it is possible to gain a licence
        if int(self.used_licences) < int(self.max_licences):
            self.free = True
        else:
            self.free = False
                    

def ui_draw(text):
    """ Draw challenger interface. """    
    
    os.system('cls')
    
    print(" ")
    print("===============================================================")
    print(" LUSAS Licence Challenger v" + CHALLENGER_VERSION               )
    print("===============================================================")
    
    print(" ")
    print(" " + text)
    print(" ")
    
    print("- Summary -----------------------------------------------------")       
    print(" - LUSAS key number: %s" % LSM_KEYID)
    print(" - %s of %s licences in use." % (lsmon.used_licences, lsmon.max_licences))
    print(" - Current LUSAS users : ")
    
    user_string = " | "
    for user in lsmon.users:
        user_string = user_string + user + " | "
    print(user_string)
    print(" ")
    
    print("- Menu --------------------------------------------------------")
    print(" - [E]mail current users"                                       )
    print(" - Start [L]imited LUSAS"                                       )
    print(" - [Q]uit Challenger"                                           )
    print(" ")
    
    print("===============================================================")    

def progress_bar(part, parts):
    """ Draws a progress bar. """    
    
    # determine local length from parts/part ratio
    progress = int(round(BAR_LENGTH / parts * part, 0))
    
    # open bar
    bar = BAR_OPEN
    
    # create bar on/off ratio
    for i in range(0, progress):
        bar = bar + BAR_ON
    for i in range(progress, BAR_LENGTH):
        bar = bar + BAR_OFF
    
    # complete bar
    bar = bar + BAR_CLOSE
    
    return bar            


def inline_menu(reload = "None"):
    """ Test for in-line menu commands while waiting. """
        
    # enter timer loop
    start_time = time.time()
    while True:
        
        # check for keyboard events
        if msvcrt.kbhit():            
            
            key = msvcrt.getche()
            
            try:
                option = key.decode()
            except:
                option = ""
            
            # capture menu presses
            if option in ['E', 'e'] : email()            
            if option in ['Q', 'q'] : sys.exit()            
            if option in ['L', 'l'] : load_lusas(True)
            
            if reload == "Reload":
                if option in ['Y', 'y'] : return
                if option in ['N', 'n'] : sys.exit()

        # break timer
        if reload == "None":
            if (time.time() - start_time) > MEN_WAIT : break


def email():
    """ Prepare a standard 'can I have LUSAS' e-mail. """
    
    # form users
    mail_to = ""
    for user in lsmon.users:
        mail_to = mail_to + user + ";"
    
    # create e-mail
    webbrowser.open('mailto:' + mail_to + '&subject=LUSAS&body=Please can you let me know once you have finished with LUSAS.%0A %0AThanks.%0A')

        
def load_lusas(limited):
    """ Start LUSAS. """

    # start limited lusas licence while waiting
    if limited == True:    
        ui_draw("Starting LUSAS with limited licence...")
        subprocess.Popen([LUS_LOCATION, 'tt=YES'])
        time.sleep(LSM_WAIT)
        return
    
    # load full lusas
    ui_draw("Attempting to catch LUSAS licence...")
    lusas = subprocess.Popen(LUS_LOCATION)
    time.sleep(LSM_WAIT)
    
    # check for success
    lsmon.refresh()
    if username in lsmon.users:
        n = 0
        
        while True:
        
            # poll until exit
            for i in range (0, LUS_WAIT):
                ui_draw("Standing by if LUSAS crashes " + progress_bar(i, LUS_WAIT))
                inline_menu()
                n = n + 1
            
            # once exited check if crashed
            if not (lusas.poll() is None):
                ui_draw("Reload LUSAS? [Y]es / [N]o")
                inline_menu("Reload")
                return
                
            # keep licence information up to date, at lower frequency
            if n >= (LSM_WAIT * 2):
                lsmon.refresh()
                n = 0                
    
    else:   
        ui_draw("Lost LUSAS licence.")
        time.sleep(LUS_WAIT)
    
       
def challenge():
    """ Challenge LUSAS licence server until a licence becomes available. """    
    
    while not lsmon.free:
        
        # prevent server spam by waiting
        for i in range (0, LSM_WAIT - 1):
            ui_draw("Challenging licence server " + progress_bar(i, LSM_WAIT))
            inline_menu()
                
        # challenge server
        ui_draw("Challenging licence server " + progress_bar(LSM_WAIT, LSM_WAIT))
        lsmon.refresh()

    # once free, load lusas licence
    load_lusas(username)
    

# configuration
username = os.environ['USERNAME']
lsmon = lsmon_py()

# automagic path configuration
base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
if base_path.find(r'Third Party\Challenger')  > -1:
    LSM_LOCATION = base_path.replace(r'Third Party\Challenger', "") + """Programs\License\lsmon.exe"""
    LUS_LOCATION = base_path.replace(r'Third Party\Challenger', "") + """Programs\lusas_m.exe"""    

  
# main loop
while True:
    lsmon.refresh()
    challenge()
    load_lusas(False)
