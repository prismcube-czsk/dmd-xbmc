# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Modify: 2011-07-31, by Ivo Brhel
#
# urlresolver XBMC Addon
# Copyright (C) 2011 t0mm0
# https://github.com/t0mm0/xbmc-urlresolver/pull/15 
#
# Modify: 2011-12-06 Ivo Brhel
#
#------------------------------------------------------------

import re, sys, os
import urlparse, urllib, urllib2


_VALID_URL = r'^((?:http://)?(?:\w+\.)?videobb\.com/(?:(?:(?:e/)|(?:video/))|(?:f/))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
_UserAgent_ =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'

def getURL(url):
    code = Extract_id(url)
    #controluri = "http://videobb.com/player_control/settings.php?v=%s&fv=v1.1.58"  %code
    controluri = "http://videobb.com/player_control/settings.php?v=%s&em=TRUE&fv=v1.1.67" %code
    #
    req = urllib2.Request(controluri)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    datajson=response.read()
    response.close()
    #print datajson
   
  
    datajson = datajson.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")
    #formatos = datadict["settings"]["res"]
    #longitud = len(formatos)
    #uri = formatos[longitud-1]["u"]
    #import base64
    
    #devuelve = base64.decodestring(uri)
    #print devuelve
    #return
   
   
    #find highest quality URL
    #max_res = [240, 480, 99999][int(get_setting('q'))]
    
    max_res = [240, 480, 99999]
    
    r = re.finditer('"l".*?:.*?"(.+?)".+?"u".*?:.*?"(.+?)"', datajson)
    chosen_res = 0
    stream_url = False
        
    if r:
        for match in r:
            res, url = match.groups()
            res = int(res.strip('p'))
            if res > chosen_res and res <= max_res:
                stream_url_part1 = url.decode('base-64')
                chosen_res = res
    else:
        print('videobb: stream url part1 not found')
        return False
        
    #print stream_url_part1
  
			
    #2nd part of URL (sece2) is encrypted in megavideostyle (aes256 or something)
    #print datadict["settings"]["video_details"]["sece2"]
    #print datadict["settings"]["config"]["rkts"]


    stream_url_part2 = decrypt(datadict["settings"]["video_details"]["sece2"], datadict["settings"]["config"]["rkts"], 113296.5*2)
		
    stream_url = stream_url_part1 + "&c=" + stream_url_part2

    return stream_url
    
    
   

def Extract_id(url):
	# Extract video id from URL
	mobj = re.match(_VALID_URL, url)
	if mobj is None:
		print 'ERROR: invalid URL: %s' % url
		return ""
	id = mobj.group(2)
	return id


def decrypt(str, k1, k2):
			
		tobin = hex2bin(str)
		keys = []
		index = 0

		while (index < 384):
			k1 = ((int(k1) * 11) + 77213) % 81371
			k2 = ((int(k2) * 17) + 92717) % 192811
			keys.append((int(k1) + int(k2)) % 128)
			index += 1

		index = 256

		while (index >= 0):
			val1 = keys[index]
			mod  = index%128
			val2 = tobin[val1]
			tobin[val1] = tobin[mod]
			tobin[mod] = val2
			index -= 1

		index = 0
		while(index<128):
			tobin[index] = int(tobin[index]) ^ int(keys[index+256]) & 1
			index += 1
			decrypted = bin2hex(tobin)
		return decrypted
	
def hex2bin(val):
		bin_array = []
		string =  bin(int(val, 16))[2:].zfill(128)
		for value in string:
			bin_array.append(value)
		return bin_array

def bin2hex(val):
		string = str("")
		for char in val:
			string+=str(char)
		return "%x" % int(string, 2)
		
def bin(x):
		'''
		bin(number) -> string

		Stringifies an int or long in base 2.
		'''
		if x < 0: return '-' + bin(-x)
		out = []
		if x == 0: out.append('0')
		while x > 0:
			out.append('01'[x & 1])
			x >>= 1
			pass
		try: return '0b' + ''.join(reversed(out))
		except NameError, ne2: out.reverse()
		return '0b' + ''.join(out)
