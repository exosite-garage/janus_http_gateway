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

import MDM      #code owned by: Telit
import MOD      #code owned by: Telit
import SER      #code owned by: Telit
import GPIO     #code owned by: Telit
import timers   #code owned by: Telit
import sys      #code owned by: Telit

def init_parameters (speed,format):

    try:

        ## ########################################################################################################      
        ## Take control of UART_SEL input
        ## Warning don't externaly drive the UART_SEL input via 50-PIN header when controlling via this script!!!!
        ## ########################################################################################################

        #MUX SELECT, GPIO 20 configured as Output, value is Set to '1'
        #DB9 connected to SER MODULE
        GPIO.setIOdir(20,1,1)

        #Init Serial Port Settings
        res = SER.set_speed(speed,format)

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> GSM864QP_SER'
        print 'METHOD -> init_parameters(' + speed + ',' + format + ')'

    return (res)

def read_DB9():
    # This function receives data via External DB9 Serial Port

    try:

        GPIO.setIOvalue(20, 1)  #Set MUX SELECT, GPIO 20 value is Set to '1'

        res = SER.receive(10)

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> GSM864QP_SER'
        print 'METHOD -> read_DB9()'

    return(res)

def send_DB9(inSTR):
    # This function sends data via External DB9 Serial Port

    try:

        GPIO.setIOvalue(20, 1)  #Set MUX SELECT, GPIO 20 value is Set to '1'

        res = SER.send(str(inSTR))

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> GSM864QP_SER'
        print 'METHOD -> send_DB9()'

    return(res)

def read_50PIN():
    # This function receives data via External 50 pin Header Serial Port

    try:

        GPIO.setIOvalue(20, 0)  #Set MUX SELECT, GPIO 20 value is Set to '0'

        res = SER.receive(10)

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> GSM864QP_SER'
        print 'METHOD -> read_50PIN()'

    return(res)

def send_50PIN(inSTR):
    # This function sends data via External 50 pin Header Serial Port

    try:

        GPIO.setIOvalue(20, 0)  #Set MUX SELECT, GPIO 20 value is Set to '0'

        res = SER.send(str(inSTR))

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> GSM864QP_SER'
        print 'METHOD -> send_50PIN()'

    return(res)