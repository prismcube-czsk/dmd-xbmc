# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Modify: 2011-07-31, by Ivo Brhel
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
    formatos = datadict["settings"]["res"]
    longitud = len(formatos)
    uri = formatos[longitud-1]["u"]
    import base64
    
    devuelve = base64.decodestring(uri)
    return devuelve

def Extract_id(url):
	# Extract video id from URL
	mobj = re.match(_VALID_URL, url)
	if mobj is None:
		print 'ERROR: invalid URL: %s' % url
		return ""
	id = mobj.group(2)
	return id
