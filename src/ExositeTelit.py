
# License is BSD, Copyright (c) 2010, Exosite LLC
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of Exosite LLC nor the names of its contributors may
#      be used to endorse or promote products derived from this software 
#      without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# 
# Platform and Web services terms and conditions are found at the following URL: 
# http://exosite.com/terms-conditions

import CW20             #code owned by: Janus Remote Communications

##------------------------------------------------------------------------------------------------------------------
##      Utility functions for sending data to Exosite's One Platform
##------------------------------------------------------------------------------------------------------------------

def rms(list):
# Calculates the rms for a list of values that are strings
    total = 0
    avg = 0
    for i in list:
        total = total + (int(i)*int(i))
    avg = total / len(list)
    return sqrt(avg)
    

def mean(list):
# Calculates the mean for a list of values that are strings
    total = 0
    for i in list:
        total = total + abs(int(i))
    return total / len(list)
    

def signalConv(response):
# Calculates the dBm value per the conversion outlined in the AT Command Reference    
    value = response[6:].split(',')[0]
    if value == '99':
        return 0
    return -113 + 2 * int(value)


def encodeValue(val):
# Encode often used characters
    val = val.replace('%','%25')
    val = val.replace('+','%2B')
    val = val.replace(' ','+')
    # Need to perform the previous replacements in that order
    val = val.replace(';','%3B')
    val = val.replace('?','%3F')
    val = val.replace('/','%2F')
    val = val.replace(':','%3A')
    val = val.replace('#','%23')
    val = val.replace('&','%26')
    val = val.replace('=','%3D')
    val = val.replace('$','%24')
    val = val.replace(',','%2C')
    val = val.replace('<','%3C')
    val = val.replace('>','%3E')
    val = val.replace('~','%7E')
    return val


def httpPost(cik, resource_dict):
# Constructs the post message for sending data to Exosite's platform
    try:
        params = ''
        count = 1
        # Create the POST variables manually because urllib is not available
        for id,val in resource_dict.items():
            params = params + '%s=%s' % (id,encodeValue(str(val)))
            if (count < len(resource_dict)):
                params = params + '&'
            count = count + 1
        
        post = 'POST /api:v1/stack/alias HTTP/1.1\r\n'
        post = post + 'Host: m2.exosite.com\r\n'
        post = post + 'X-Exosite-CIK: ' + cik + '\r\n'
        post = post + 'Content-Type: application/x-www-form-urlencoded; charset=utf-8\r\n'
        post = post + 'Content-Length: ' + str(len(params)) + '\r\n\r\n'
        post = post + params + '\r\n'
        
        return post
        
    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ExositeTelit'
        print 'METHOD -> httpPost(' + cik + ',' + str(resource_dict) + ')'
    
    return


def setLatLng(msg):
# This function parses the GPGLL message to get the Latitude and Longitude values
# NOTE: Unable to convert into decimal degrees because no float type is included
# with this version of Python
    try:
        GPGLL_list = msg.split(',')
        lat = GPGLL_list[1]
        lat_dir = GPGLL_list[2]
        lng = GPGLL_list[3]
        lng_dir = GPGLL_list[4]
        
        # Determine if value is negative
        if (lat_dir=='S'):
            CW20.GPSdata.Latitude = '-' + lat
        else:
            CW20.GPSdata.Latitude = lat
        
        # Remove the leading zero
        if (lng[0]=='0'):
            lng = lng[1:]
        
        if (lng_dir=='W'):
            CW20.GPSdata.Longitude = '-' + lng
        else:
            CW20.GPSdata.Longitude = lng
    
    except:
        print 'Script encountered an exception.'
        print 'Exception Type: ' + str(sys.exc_type)
        print 'MODULE -> ExositeTelit'
        print 'METHOD -> setLatLng(' + cik + ',' + str(resource_dict) + ')'
    
    return
