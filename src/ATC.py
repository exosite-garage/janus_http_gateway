## Written By Thomas W. Heck
##
##  REVISION HISTORY:
##      1.0.0   ??/??/2007  TWH --  Init Release
##      1.1.0   05/02/2008  TWH --  Changed the method for Command Timeout (using timers.pyo method)
##      1.2.0   11/12/2008  TWH --  Fixed the sendEMAIL method

import MDM      #code owned by: Telit
import MOD      #code owned by: Telit
import timers   #code owned by: Telit
import sys      #code owned by: Telit

import DEBUG    #code owned by: Janus Remote Communications

class properties:
    IMEI = ''
    SIM = ''
    Carrier = ''
    CellId = ''
    CMD_TERMINATOR = 'OK\r\n'    # This is the string termination of a AT command response



################################################################################################
## Methods for sending and receiving AT Commands
################################################################################################
    
def sendAtCmd(theCommand, theTerminator, retry, timeOut):
# This function sends an AT command to the MDM interface

    # Input Parameter Definitions
    #   theCommand: The AT command to send to MDM interface
    #   theTerminator: string or character at the end of AT Command
    #   retry:  How many times the command will attempt to retry if not successfully send 
    #   timeOut: number of [1/10 seconds] command could take to respond

    try:

        #Clear input buffer
        res = "junk"
        while(res != ""):
            res = MDM.receive(1)

        while (retry != -1):
            print 'Sending AT Command: ' + theCommand
            res = MDM.send(theCommand, 0)
            res = MDM.sendbyte(0x0d, 0)

            #Wait for AT command response
            res = mdmResponse(theTerminator, timeOut)

            #Did AT command respond without error?    
            pos1 = res.rfind(theTerminator,0,len(res))
            if (pos1 != -1):
                retry = -1
                res = parseResponse(res)
            else:
                retry = retry - 1

    except:
            print 'Script encountered an exception.'
            print 'Exception Type: ' + str(sys.exc_type)
            print 'MODULE -> ATC' + '\r'
            print 'METHOD -> sendAtCmd(' + theCommand + ',' +theTerminator + ',' + retry + ',' + timeOut + ')' + '\r'

    print res

    return res

def mdmResponse(theTerminator, timeOut):
# This function waits for AT Command response and handles errors and ignores unsolicited responses

  # Input Parameter Definitions
  #   theTerminator: string or character at the end of a received string which indicates end of a response
  #   timeOut: number of seconds command could take to respond

    try:

        print 'Waiting for AT Command Response'

        #Start timeout counter        
        timerA = timers.timer(0)
        timerA.start(timeOut)

        #Wait for response
        res = ''
        while ((res.find(theTerminator)<=-1) and (res.find("ERROR")<=-1) and (res != 'timeOut')):
            MOD.watchdogReset()
            res = res + MDM.receive(10)

            pass            
            if timerA.isexpired():
                res = 'timeOut'

    except:
            print 'Script encountered an exception.'
            print 'Exception Type: ' + str(sys.exc_type)
            print 'MODULE -> ATC'
            print 'METHOD -> mdmResponse(' + theTerminator + ',' + timeOut + ')'

    return res

def parseResponse(inSTR):
# This function parses out data return from AT commands

  # Input Parameter Definitions
  #   inSTR:  The response string from and AT command

    try:

        tmpReturn = ''
        lenght = len(inSTR)

        if lenght != 0:
            pos1 = inSTR.find('ERROR',0,lenght)
            if (pos1 != -1):
                tmpReturn = 'ERROR'
            else:
                list_in = inSTR.split( '\r\n' )
                tmpReturn = list_in[ 1 ]

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> parseResponse(' + inSTR + ')'

    return tmpReturn

################################################################################################
## Misc. Methods for GSM Modules
################################################################################################
    
def getNetworkInfo():

#ATTENTION REVIEW / REWRITE THE FOLLOWING WHILE LOOPS, could cuase loop forever

    try:
        properties.SIM = ""
        properties.SIM = sendAtCmd('AT+CIMI',properties.CMD_TERMINATOR,0,20)

        properties.IMEI = ""
        properties.IMEI = sendAtCmd('AT+CGSN',properties.CMD_TERMINATOR,0,20)

        SERVINFO = ""
        SERVINFO_list = SERVINFO.split(',')

        SERVINFO = sendAtCmd('AT#SERVINFO',properties.CMD_TERMINATOR,0,2)
        SERVINFO = SERVINFO.replace('"','')
        SERVINFO = SERVINFO.replace(':',',')
        SERVINFO = SERVINFO.replace(' ','')
        SERVINFO_list = SERVINFO.split(',')

        properties.Carrier = SERVINFO_list[4]

        MONI = ""
        MONI_list = MONI.split(' ')

        MONI = sendAtCmd('AT#MONI',properties.CMD_TERMINATOR,0,2)
        MONI = MONI.replace(' ',',')
        MONI = MONI.replace(':',',')
        MONI_list = MONI.split(',')

        properties.CellId = MONI_list[10]

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> getNetworkInfo()'

    return

################################################################################################
## Methods for Sending and receiving SMS Messages
################################################################################################

def configSMS():

    try:

        #Enable TEXT format for SMS Message
        res = sendAtCmd('AT+CMGF=1' ,properties.CMD_TERMINATOR,0,5)
        res = sendAtCmd('AT+CNMI=2,1' ,properties.CMD_TERMINATOR,0,5)

        #SIM status control - to avoid the 'sim busy' error
        print 'SIM Verification Cycle'
        SIM_status = sendAtCmd('AT+CPBS?' ,properties.CMD_TERMINATOR,0,5)

        if SIM_status.find("+CPBS")<0:
            print 'SIM busy! Please wait!\n'

        while SIM_status.find("+CPBS:")< 0 :
            SIM_status = sendAtCmd('AT+CPBS?' ,properties.CMD_TERMINATOR,0,5)
            MOD.sleep(2)
        print 'SIM Ready'

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> configSMS()'

    return

def sendSMS(theSmsMsg,theDestination,theTerminator,retry,timeOut):
#This function sends an SMS Message

  # Input Parameter Definitions
  #   theSmsMsg: The text SMS Message
  #   theTerminator: string or character at the end of AT Command
  #   retry:  How many times the command will attempt to retry if not successfully send 
  #   timeOut: number of [1/10 seconds] command could take to respond

    try:

        while (retry != -1):
            print 'AT+CMGS="' + str(theDestination) + '",145'
          
            res = MDM.send('AT+CMGS=' + str(theDestination) + ',145', 0)
            res = MDM.sendbyte(0x0d, 0)
            res = mdmResponse('\r\n>', timeOut)
            print res 

            res = MDM.send(theSmsMsg, 0)
            res = MDM.sendbyte(0x1a, 0)

            #Wait for AT command response
            res = mdmResponse(theTerminator, timeOut)

            #Did AT command respond without error?    
            pos1 = res.rfind(theTerminator,0,len(res))
            if (pos1 != -1):
              retry = -1
              res = parseResponse(res)
            else:
              retry = retry - 1

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> sendSMS(' + theSmsMsg + ',' + theDestination + ',' +theTerminator + ',' + retry + ',' + timeOut + ')'

    print res
  
    return res

################################################################################################
## Methods for sending and receiving EMAILS
################################################################################################
    
def sendEMAIL(theEmailToAddress,theEmailSubject,theEmailBody,theTerminator,userID,userPassword,retry,timeOut):
#This function sends email

  # Input Parameter Definitions
  #   theEmailSubject: The text Email Subject
  #   theEmailBody: The text Email Body
  #   theTerminator: string or character at the end of AT Command
  #   retry:  How many times the command will attempt to retry if not successfully send 
  #   timeOut: number of [1/10 seconds] command could take to respond

    try:

        tmpReturn = -1
            
        while (retry != -1):

            #Activate PDP if needed  
            res = sendAtCmd('AT#SGACT?',properties.CMD_TERMINATOR,0,20) 
            if (res!="#SGACT: 1,1"):
                delaySec(1)
                res = sendAtCmd('AT#SGACT=1,1,"' + str(userID) + '","' + str(userPassword) + '"' ,properties.CMD_TERMINATOR,0,180)
                DEBUG.sendMsg(res + '\r\n',RUN_MODE) 

            if (res=='ERROR'):
                return tmpReturn  

            print 'AT#EMAILD="' + theEmailToAddress + '","' + theEmailSubject + '",0'

            res = MDM.send('AT#EMAILD="' + theEmailToAddress + '","' + theEmailSubject + '",0', 0)
            res = MDM.sendbyte(0x0d, 0)
            res = mdmResponse('\r\n>', timeOut)
            print res 

            res = MDM.send(theEmailBody, 0)
            res = MDM.sendbyte(0x1a, 0)

            #Start timeout counter        
            timerA = timers.timer(0)
            timerA.start(timeOut)

            #Wait for response
            res = ''
            while ((res.find(theTerminator)<=-1) and (res.find("ERROR")<=-1) and (res != 'timeOut')):
                MOD.watchdogReset()
                res = res + MDM.receive(10)
                pass           
                if timerA.isexpired():
                    res = 'timeOut'
                    
            if((res.find("ERROR") > -1) or (res == 'timeOut')):
                retry = retry - 1
            else:
                retry = -1
                tmpReturn = 0                
                
    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> sendEMAIL(' + theEmailToAddress + ',' + theEmailSubject + ',' + theEmailBody + ',' +theTerminator + ',' + retry + ',' + timeOut + ')'

    print res
  
    return tmpReturn

################################################################################################
## Methods for handling GPRS communication
################################################################################################
    
def initGPRS (PDPindex,APN,userID,userPassword,RUN_MODE):

    try:        
        
        #Define GPRS Settings, MUST change APN String in script for your Carrier Specific setting
        res = sendAtCmd('AT+CGDCONT=' + str(PDPindex) + ',"IP","' + str(APN) + '","0.0.0.0",0,0' ,properties.CMD_TERMINATOR,0,20)
        #How long does system wait before sending undersized packet measured in 100ms settings
        res = sendAtCmd('AT#DSTO=10' ,properties.CMD_TERMINATOR,0,20)

        #Define Min/required Quality of Service
        res = sendAtCmd('AT+CGQMIN=1,0,0,0,0,0' ,properties.CMD_TERMINATOR,0,20)
        res = sendAtCmd('AT+CGQREQ=1,0,0,3,0,0' ,properties.CMD_TERMINATOR,0,20)

        #escape guard time, after set time escape sequence is excepted, set in 20ms settings
        res = sendAtCmd('ATS12=40' ,properties.CMD_TERMINATOR,0,20)

        #disable the escape sequence from transmitting during a data session
        res = sendAtCmd('AT#SKIPESC=1' ,properties.CMD_TERMINATOR,0,20)

        #Set connect timeOuts and packet sizes for PDP#1 and Socket#1
        res = sendAtCmd('AT#SCFG=1,1,512,90,100,50' ,properties.CMD_TERMINATOR,0,20)
        
        #Activate PDP if needed  
        res = sendAtCmd('AT#SGACT?',properties.CMD_TERMINATOR,0,20) 
        if (res!="#SGACT: 1,1"):
            delaySec(1)
            res = sendAtCmd('AT#SGACT=1,1,"' + str(userID) + '","' + str(userPassword) + '"' ,properties.CMD_TERMINATOR,0,180)
            DEBUG.sendMsg(res + '\r\n',RUN_MODE) 

        if (res=='ERROR'):
            return  
        
    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> initGPRS(' + PDPindex + ',' + APN + ',' + res + ')'

    return    

def openSocket(addr,port,sockNum,userID,userPassword,protocol,RUN_MODE):
    #Function Open a socket and responds with CONNECT/NO CARRIER/ERROR

    try:
        #Close Socket
        res = sendAtCmd('AT#SS',properties.CMD_TERMINATOR,0,20)
        if (res!="#SS: 1,0"):
            res = sendAtCmd('AT#SH=1',properties.CMD_TERMINATOR,0,20)

        if (res=='ERROR'):
            return
        
        #Activate PDP if needed  
        res = sendAtCmd('AT#SGACT?',properties.CMD_TERMINATOR,0,20) 
        if (res!="#SGACT: 1,1"):
            delaySec(1)
            res = sendAtCmd('AT#SGACT=1,1,"' + str(userID) + '","' + str(userPassword) + '"' ,properties.CMD_TERMINATOR,0,180)
            DEBUG.sendMsg(res + '\r\n',RUN_MODE) 

        if (res=='ERROR'):
            return            

        #Open Socket to Server
        if (str(protocol)=='TCPIP'):
            res = sendAtCmd('AT#SD=1,0,' + port + ',"' + addr + '",0','CONNECT\r\n',0,180)
        else:
            res = sendAtCmd('AT#SD=1,1,' + port + ',"' + addr + '",0,5559','CONNECT\r\n',0,180)

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> openSocket(' + addr + ',' + port + ',' + sockNum + ',' + userID + ',' + userPassword + ',' + protocol + ')'

    return res

def exitSocketDataMode():

    try:
        #Exit data mode
        delaySec(11)         ##this time is based on esc sequence guard time
        #Start timeout counter        
        timerA = timers.timer(0)
        timerA.start(20)

        #Sending +++
        print 'Sending Data Mode escape sequence'
        res = MDM.send('+++', 10)


        #Wait for response
        res = ''
        while ((res.find("OK")<=-1) and (res != 'timeOut')):
            MOD.watchdogReset()
            res = res + MDM.receive(50)

            pass            
            if timerA.isexpired():
                res = 'timeOut'

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> exitSocketDataMode()'

    print res

    return res

def closeSocket(sockNum):

    try:
        #Close Socket
        res = sendAtCmd('AT#SH=' + str(sockNum),properties.CMD_TERMINATOR,0,20)

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> closeSocket(' + sockNum + ')'


    return res

################################################################################################
## Misc support Methods
################################################################################################

def delaySec(seconds):

    try:

        if(seconds<=0): return    

        timerA = timers.timer(0)
        timerA.start(seconds)
        while 1:
            MOD.watchdogReset()
            if timerA.isexpired():
                break

    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ATC'
        print 'METHOD -> delaySec(' + seconds + ')'


    return  