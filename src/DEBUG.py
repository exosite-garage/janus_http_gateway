#Copyright © 2008, Janus Remote Communications
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions
#are met:
#
#Redistributions of source code must retain the above copyright notice,
#this list of conditions and the following disclaimer.
#
#Redistributions in binary form must reproduce the above copyright
#notice, this list of conditions and the following disclaimer in
#the documentation and/or other materials provided with the distribution.
#
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS``AS
#IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys              #code owned by: Telit
import GSM864QP_SER     #code owned by: Janus Remote Communications

def sendMsg(inSTR, RUN_MODE):
# This function sends a debug message to print statement or DB9 Serial Port 

    # Input Parameter Definitions
    #   inSTR: Debug Message
    #   RUN_MODE:
    #       (0) Send message via print statement "Script running in IDE"
    #       (1) Send message via DB9 serial port "Script running in Telit module"
    
    try:

        if (RUN_MODE):
            GSM864QP_SER.send_DB9(inSTR)
        else:
            print inSTR
            
    except:
            print 'Script encountered an exception.'
            print 'Exception Type: ' + str(sys.exc_type)
            print 'MODULE -> DEBUG' + '\r'
            print 'METHOD -> sendMsg(' + inSTR + ',' + RUN_MODE + ')' + '\r'

    return

def CLS(RUN_MODE):
# This function sends a VT100 Terminal Clear screen message to DB9 Serial Port 

    # Input Parameter Definitions
    #   RUN_MODE:
    #       (0) Don't send clear screen message
    #       (1) Send VT100 clear screen message via DB9 serial port "Script running in Telit module"
    
    try:

        if (RUN_MODE):
            GSM864QP_SER.send_DB9("\033[2J\r")
            
    except:
            print 'Script encountered an exception.'
            print 'Exception Type: ' + str(sys.exc_type)
            print 'MODULE -> DEBUG' + '\r'
            print 'METHOD -> CLS(' + RUN_MODE + ')' + '\r'

    return