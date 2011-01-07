#External GPS Class Example
# Written for NavSync's CW20 16 Channel GPSdata Receiver
# Goto:  www.navsync.com for more information
#
#Copyright © 2007, Janus Remote Communications
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

import MOD              #code owned by: Telit
import sys              #code owned by: Telit
import timers           #code owned by: Telit
import GPIO             #code owned by: Telit

import GSM864QP_SER     #code owned by: Janus Remote Communications

class GPSdata:
    UTC = 1
    Status = ''
    Latitude = ''
    NS = ''
    Longitude = ''
    EW = ''
    Speed = ''
    Course = ''
    Date = ''
    Mode = ''
    VDOP = ''
    HDOP = ''
    GPGGA = ''
    GPGLL = ''
    GPGSA = ''
    GPGSV = ''
    GPRMC = ''
    GPZDA = ''
    GPVTG = ''

def initGPS (speed,format):
    
    try:

        #GPS RESET, GPIO 18 configured as Output, value is Cleared to '0'
        #GPS held in RESET
        GPIO.setIOdir(18,1,1)
        
        #GPS RESET, GPIO 18 configured as Output, value is Cleared to '0'
        #GPS is running
        GPIO.setIOvalue(18, 0)
        
        #Init Serial Port Settings
        res = GSM864QP_SER.init_parameters(speed,format)
        MOD.sleep(10)
        
        res = GSM864QP_SER.send_50PIN('\r\n')

        #Disable all NMEA output sentences
        #NMEA GPS sentences will only transmit when polled by CW20.update() method
        res = GSM864QP_SER.send_50PIN('$PNMRX103,ALL,0\r\n')
        
        ## Start timeout timer            
        CW20_timerA = timers.timer(0)
        CW20_timerA.start(2)  

        # Empty Serial Port Buffer
        res = "junk"
        while(res != ""):
            res = GSM864QP_SER.read_50PIN()
            if (CW20_timerA.isexpired()):
                break

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> CW20'
        print 'METHOD -> initGPS(' + speed + ',' + format + ')'

    return


def update():
    # This function receives ALL NMEA sentences and parses out data fields
    # You might need to add more properties to this class to get more data out of the update method
    # You MUST have the jumpers on the external header connecting Pin(49 & 47) and Pin(45 & 43)
    try:

        #Get NMEA RMC sentence
        NMEA = ''
        NMEA_list = ''
        GPSdata.GPGGA = ''
        GPSdata.GPGLL = ''
        GPSdata.GPGSA = ''
        GPSdata.GPGSV = ''
        GPSdata.GPRMC = ''
        GPSdata.GPZDA = ''
        GPSdata.GPVTG = ''

        ## Start timeout timer            
        CW20_timerA = timers.timer(0)
        CW20_timerA.start(10)

        #Clear Buffer - NMEA Commands are disabled in initReceiver
        res=''
        while(res != ''):
            res = GSM864QP_SER.read_50PIN()
            if (CW20_timerA.isexpired()):
                break

        #Enable NMEA sentence to transmit once every 10 seconds
        res = GSM864QP_SER.send_50PIN('$PNMRX103,ALL,10\r\n')
        NMEA = ''
        while(1):
            res = GSM864QP_SER.read_50PIN()
            NMEA = NMEA + res
            lenNMEA = len(NMEA)
            pos1 = NMEA.rfind('GPVTG',0)
            pos2 = NMEA.rfind('\r\n',pos1)
            if ((pos1 >=0) and (pos2 >= pos1)):
            #NMEA data is complete
                break

            if (CW20_timerA.isexpired()):
                GPSdata.GPGGA = 'TIMEOUT\r\n'
                GPSdata.GPGLL = 'TIMEOUT\r\n'
                GPSdata.GPGSA = 'TIMEOUT\r\n'
                GPSdata.GPGSV = 'TIMEOUT\r\n'
                GPSdata.GPRMC = 'TIMEOUT\r\n'
                GPSdata.GPZDA = 'TIMEOUT\r\n'
                GPSdata.GPVTG = 'TIMEOUT\r\n'
                return

        NMEA_list = NMEA.split('\r\n')

        for x in NMEA_list:
            sentence_list = x.split(',')

            if (sentence_list[0] == '$GPGGA'):
                GPSdata.GPGGA = str(x) + '\r\n'
            elif (sentence_list[0] == '$GPGLL'):
                GPSdata.GPGLL = str(x) + '\r\n'
            elif (sentence_list[0] == '$GPGSA'):
                GPSdata.GPGSA = str(x) + '\r\n'
            elif (sentence_list[0] == '$GPGSV'):
                GPSdata.GPGSV = GPSdata.GPGSV + str(x) + '\r\n'
            elif (sentence_list[0] == '$GPRMC'):
                GPSdata.GPRMC = str(x) + '\r\n'
            elif (sentence_list[0] == '$GPZDA'):
                GPSdata.GPZDA = str(x) + '\r\n'
            elif (sentence_list[0] == '$GPVTG'):
                GPSdata.GPVTG = str(x) + '\r\n'

        #Disable all NMEA Sentences
        res = GSM864QP_SER.send_50PIN('$PNMRX103,ALL,0\r\n')
        while(res != ''):
            res = GSM864QP_SER.read_50PIN()
            if (CW20_timerA.isexpired()):
                break

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> CW20'
        print 'METHOD -> update()'
        GPSdata.GPGGA = 'EXCEPTION\r\n'
        GPSdata.GPGLL = 'EXCEPTION\r\n'
        GPSdata.GPGSA = 'EXCEPTION\r\n'
        GPSdata.GPGSV = 'EXCEPTION\r\n'
        GPSdata.GPRMC = 'EXCEPTION\r\n'
        GPSdata.GPZDA = 'EXCEPTION\r\n'
        GPSdata.GPVTG = 'EXCEPTION\r\n'

    return