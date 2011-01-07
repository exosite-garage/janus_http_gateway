#GPS Demo for the Terminus Terminal modified for sending GPS and
#additional data to the Exosite platform
# Janus Model#  GSM864QP V1.0
#
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

import MDM              #code owned by: Telit
import MOD              #code owned by: Telit
import timers           #code owned by: Telit
import sys              #code owned by: Telit

import CW20             #code owned by: Janus Remote Communications
import ATC              #code owned by: Janus Remote Communications
import GSM864QP_SER     #code owned by: Janus Remote Communications
import DEBUG            #code owned by: Janus Remote Communications

import ExositeTelit     #code owned by: Exosite

##------------------------------------------------------------------------------------------------------------------
## Release  Information:
##  V1.0 (Thomas W. Heck, 10/15/2008)               :   Initial release
##  V1.1 Exosite modifications                      :   Send GPS and additional data to Exosite platform
##------------------------------------------------------------------------------------------------------------------

##------------------------------------------------------------------------------------------------------------------
## NOTES
##  1.)  exceptions.pyo must be loaded on the Telit module in order for this code to work correctly
##  2.)  Don't include the following line of code in any of your modules: 'import exceptions'
##  3.)  See Main Script, Application Specific Configuration section.  Demo must be altered for customer settings
##  4.)  print statements are displayed when using the IDE to debug application
##  5.)  Please read "Terminus GPS Demonstration Guide.pdf"
##------------------------------------------------------------------------------------------------------------------

class myApp:
    BAND = ''
    NETWORK = ''
    APN = ''
    IP = ''
    PORT = ''
    PROTOCOL = ''
    SMS = ''
    INTERVAL = ''
    GPRS_USERID = ''
    GPRS_PASSWORD = ''
    CIK = ''                # <-- Exosite


#Main Script
# ###############################################################
try:

    ##-----------------------------------------------------------------------------------------------------
    ## Application Specific Configuration
    ##-----------------------------------------------------------------------------------------------------

    ## BAND
    ## Please refer to AT Command guide for AT#BND
    ## If Terminal used in North America (BAND = '3')
    myApp.BAND = '3'

    ## NETWORK
    ## If Terminal used on ATT / Cingular in North America (NETWORK = 'ATT')
    ## Else (NETWORK = 'GSM')
    myApp.NETWORK = 'GSM'

    ## APN
    ## Gateway Address for GPRS traffic
    ## This setting is GSM Provider and possible customer specific when a VPN is used
    ## This demo is defaulted with proxy that is used for ATT wireless settings from pre-Cingular days
    ## You MUST obtain the APN setting for your GSM account.  Please call GSM provider!  Janus can't help you with this.
    myApp.APN = ''

    ## IP
    ## IP address of server on the Internet which Terminus will connect to send GPS information
    ## Address in this example is not operational for customer evaluation.  Customer must have their own server
    ## setup to interact with this demo.
    myApp.IP = 'm2.exosite.com'

    ## PORT
    ## PORT number of server on the Internet which Terminus will connect to send GPS information
    ## PORT number in this example is not operational for customer evaluation.  Customer must have their own server
    ## setup to interact with this demo.
    myApp.PORT = '80'

    ## PROTOCOL
    ## If customer is using TCPIP (PROTOCOL = 'TCPIP')
    ## Else leave blank (PROTOCOL = '')
    myApp.PROTOCOL = 'TCPIP'

    ## SMS
    ## SMS Designation phone number (SMS = '+16305551212')
    myApp.SMS = '+1'

    ## INTERVAL
    ## How many seconds the demo will wait before sending new GPS data to server.
    ## In this demo, GPS data will be sent every 60 seconds (INTERVAL = '60')
    myApp.INTERVAL = '30'
    
    ## GPRS_USERID
    ## USERID for GPRS connection - ask your network operator for setting
    ## If GPRS_USERID is not required leave empty 
    myApp.GPRS_USERID = ''
    
    ## GPRS_PASSWORD
    ## PASSWORD for GPRS connection - ask your network operator for setting
    ## If GPRS_PASSWORD is not required leave empty 
    myApp.GPRS_PASSWORD = ''
    
    # Exosite -->
    ## CIK
    ## THE CIK VALUE FOR THIS DEVICE - get this value from your Exosite account
    ## THIS IS REQUIRED FOR SENDING DATA TO EXOSITE
    myApp.CIK = ''
    # <-- Exosite
    
    #Reboot system after <entered value> secs if unable to register with a network
    #Allow at least 5 minutes (300 seconds)
    MOD.watchdogEnable(300)

    try:
        RUN_MODE = 0
        test = float(RUN_MODE)  #float not implemented in Telit module
    except:
        #Running in IDE
        RUN_MODE = 1

    DEBUG.CLS(RUN_MODE)   #Clear screen command for VT100 terminals
    DEBUG.sendMsg("GPSDemo Script has started\r\n",RUN_MODE)  
  
    #Apply Network Specific settings see myApp.xxxx assignment above
    if (myApp.NETWORK == "ATT"):
        #Set module to work on US ATT Network  
        res = ATC.sendAtCmd("AT#ENS?",ATC.properties.CMD_TERMINATOR,3,2)        #query ENS setting
        if (res == "#ENS: 0"):
            res = ATC.sendAtCmd('AT#ENS=1',ATC.properties.CMD_TERMINATOR,3,2)   #sets all ATT requirements
            MOD.sleep(15)                                                       #required to halt Python thread and allow NVM Flash to update
            res = ATC.sendAtCmd('AT#REBOOT',ATC.properties.CMD_TERMINATOR,3,2)  #must reboot to take effect
        res = ATC.sendAtCmd("AT#SELINT?",ATC.properties.CMD_TERMINATOR,3,2)     #query SELINT setting
        if (res != "#SELINT: 2"):
            res = ATC.sendAtCmd('AT#SELINT=2',ATC.properties.CMD_TERMINATOR,3,2)#use of most recent AT command set
            MOD.sleep(15)                                                       #required to halt Python thread and allow NVM Flash to update
            res = ATC.sendAtCmd('AT#REBOOT',ATC.properties.CMD_TERMINATOR,3,2)  #must reboot to take effect
        
    else:
        #Set module to work on all other Networks
        res = ATC.sendAtCmd('AT#ENS?',ATC.properties.CMD_TERMINATOR,3,2) 
        if (res == "#ENS: 1"):
            res = ATC.sendAtCmd('AT#ENS=0',ATC.properties.CMD_TERMINATOR,3,2)   #disable ATT requirements
            MOD.sleep(15)                                                       #required to halt Python thread and allow NVM Flash to update
            res = ATC.sendAtCmd('AT#REBOOT',ATC.properties.CMD_TERMINATOR,3,2)  #must reboot to take effect
        res = ATC.sendAtCmd("AT#SELINT?",ATC.properties.CMD_TERMINATOR,3,2)     #query SELINT setting
        if (res != "#SELINT: 2"):
            res = ATC.sendAtCmd('AT#SELINT=2',ATC.properties.CMD_TERMINATOR,3,2)#use of most recent AT command set
            MOD.sleep(15)                                                       #required to halt Python thread and allow NVM Flash to update
            res = ATC.sendAtCmd('AT#REBOOT',ATC.properties.CMD_TERMINATOR,3,2)  #must reboot to take effect
        res = ATC.sendAtCmd('AT#STIA=2,10',ATC.properties.CMD_TERMINATOR,3,2)   #enable SAT - SIM Application Tool-Kit
        res = ATC.sendAtCmd('AT#BND='+myApp.BAND,ATC.properties.CMD_TERMINATOR,3,2)       #set bands to 850/1900
        res = ATC.sendAtCmd('AT#AUTOBND=1',ATC.properties.CMD_TERMINATOR,3,2)	#enable Quad band system selection
        res = ATC.sendAtCmd('AT#PLMNMODE=1',ATC.properties.CMD_TERMINATOR,3,2)	#enable EONS (enhanced operator naming scheme) 

    DEBUG.sendMsg("Connecting to network",RUN_MODE)

    #Wait until registered to GSM Network
    exitLoop = 1
    while (exitLoop == 1):
        res = ATC.sendAtCmd('AT+CREG?',ATC.properties.CMD_TERMINATOR,0,5)
        DEBUG.sendMsg(".",RUN_MODE)
        if (res[res.rfind(',')+1:len(res)] == '5' or res[res.rfind(',')+1:len(res)] == '1'):
            exitLoop = 0
        
    DEBUG.sendMsg("\r\nConnected to network\r\n",RUN_MODE)

    MOD.watchdogReset()

    #Setup SMS         
    ATC.configSMS()

    #Send SMS
    #Uncomment if SIM card is provisioned for SMS
    #ATC.sendSMS("GPSDemo application is running",myApp.SMS,ATC.properties.CMD_TERMINATOR,3,180)

    #Init GPRS
    #Pass in: PDP Index, APN
    ATC.initGPRS('1', myApp.APN, myApp.GPRS_USERID, myApp.GPRS_PASSWORD, RUN_MODE)
    
    #Initalize CW20 Receiver
    DEBUG.sendMsg("Initialize CW20 GPS Module\r\n",RUN_MODE)
    CW20.initGPS('9600','8N1')
    
    #Update Network Information
    res = ATC.getNetworkInfo()

    # Start timeout timer            
    timerB = timers.timer(0)
    timerB.start(1)
    
    ping = 1    # <-- Exosite: initialize value
    
    # Loop forever, without this loop the script would run once and exit script mode.  On reboot or power-on the script would run once more
    while (1):
                
        exitCode = -1
        while (exitCode==-1):

            MOD.watchdogReset()

            #If interval timer expires then send packet to server       
            if (timerB.isexpired()):
                
                # Exosite -- >
                # Acquire values to send to Exosite and display on terminal
                
                # Get ping
                DEBUG.sendMsg('Ping = ' + str(ping) + '\r\n',RUN_MODE)
                                
                # Get signal strength
                res = ATC.sendAtCmd('AT+CSQ',ATC.properties.CMD_TERMINATOR,0,5)
                sig = ExositeTelit.signalConv(res)
                DEBUG.sendMsg("Get signal strength: (" + str(sig) + ")dBm \r\n",RUN_MODE)
                
                # Update NMEA Data
                DEBUG.sendMsg("Polling GPS receiver for current location\r\n",RUN_MODE)
                CW20.update()
                DEBUG.sendMsg('Current GPGLL sentence: ' + CW20.GPSdata.GPGLL + "\r\n",RUN_MODE)
                ExositeTelit.setLatLng(CW20.GPSdata.GPGLL)                                          # Parses lat/lng values
                latlng = CW20.GPSdata.Latitude + '_' + CW20.GPSdata.Longitude
                # <-- Exosite
                
                DEBUG.sendMsg("Opening Connection to server: " + myApp.IP + ":" + myApp.PORT + "\r\n",RUN_MODE)
                            
                #Connect to customer demo server
                #Pass in: IP Address, IP Port, sockNum, GPRSuserName, GPRSuserPassword
                res = ATC.openSocket(myApp.IP,myApp.PORT,'1','','',myApp.PROTOCOL,RUN_MODE)

                try:
                    #If socket open upload data
                    if (res == 'CONNECT'):

                        DEBUG.sendMsg('Connection opened\r\n',RUN_MODE)
                        
                        # Build string to send to customer server
                        #STA = ATC.properties.IMEI +',' + CW20.GPSdata.GPGLL            # <-- Exosite: removed
                        
                        # Exosite -->
                        # Enter your resource ids as the <key> and data as the <value> of a Python dictionary
                        # Ex: Resourced ID #1 stores latitude/longitude data, Resource ID #2 stores ping data 
                        # resource_dict = {'1':latlng, '2':ping}
                        resource_dict = {
                                            '1': latlng,
                                            '2': ping,
                                            '3': sig
                                        }
                        post = ExositeTelit.httpPost(myApp.CIK, resource_dict)
                        # <-- Exosite
                        
                        # Send string to customer server
                        DEBUG.sendMsg('Sending data: ' + post + '\r\n',RUN_MODE)        # <-- Exosite: changed STA to post
                        res = MDM.send(post,0)                                          # <-- Exosite: changed STA to post
                        
                        #Exit data mode
                        DEBUG.sendMsg('Exiting data mode\r\n',RUN_MODE) 
                        res = ATC.exitSocketDataMode()

                        #Close Socket
                        #Pass in: sockNum
                        res = ATC.closeSocket('1')
                        DEBUG.sendMsg('Connection closed\r\n',RUN_MODE) 

                        exitCode = 0
                        
                        # Exosite -->
                        # Increase or reset the counter
                        if (ping == 100):
                            ping = 1
                        else:
                            ping = ping + 1
                        # <-- Exosite
                        
                    else:
                        DEBUG.sendMsg("Connection failed to open\r\n",RUN_MODE)

                        # Is Terminus still connected to GSM Network?                                                                        
                        res = ATC.sendAtCmd('AT+CREG?',ATC.properties.CMD_TERMINATOR,0,5)
                        DEBUG.sendMsg("GSM Network Registration (AT+CREG?): " + res + "\r\n",RUN_MODE)

                        #What is the signal strenght?
                        res = ATC.sendAtCmd('AT+CSQ',ATC.properties.CMD_TERMINATOR,0,5)
                        DEBUG.sendMsg("Signal Strength (AT+CSQ): " + res + "\r\n",RUN_MODE)

                        #Is a PDP context activated?
                        res = ATC.sendAtCmd('AT#SGACT?',ATC.properties.CMD_TERMINATOR,0,20)
                        DEBUG.sendMsg("PDP Context status (AT#SGACT?): " + res + "\r\n",RUN_MODE)

                except:
                    DEBUG.sendMsg('Script encountered an exception while uploading data to server\r\n',RUN_MODE)
                    DEBUG.sendMsg('Exception Type: ' + str(sys.exc_type) + "\r\n",RUN_MODE)
                    DEBUG.sendMsg('MODULE -> GPSDemo\r\n',RUN_MODE)
                    exitCode = 0

        ## Re-Start timeout timer            
        timerB = timers.timer(0)
        timerB.start(int(myApp.INTERVAL))

        DEBUG.CLS(RUN_MODE)   #Clear screen command for VT100 terminals

except:
    DEBUG.sendMsg('Script encountered an exception\r\n',RUN_MODE)
    DEBUG.sendMsg('Exception Type: ' + str(sys.exc_type) + "\r\n",RUN_MODE)
    DEBUG.sendMsg('MODULE -> GPSDemo\r\n',RUN_MODE)
    MOD.sleep(15)                                                       #required to halt Python thread and allow NVM Flash to update
    res = ATC.sendAtCmd('AT#REBOOT',ATC.properties.CMD_TERMINATOR,0,5)  #must reboot or Script will not restart until a power cycle occurs

      