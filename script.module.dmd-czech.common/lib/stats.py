# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcaddon, time
import urllib, urllib2 
from uuid import getnode as uuid_node
from hashlib import md5
__addon__       = xbmcaddon.Addon()
_UserAgent_     = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def uniq_id(mac_addr):
	if not ":" in mac_addr: mac_addr = xbmc.getInfoLabel('Network.MacAddress')
	# hack response busy
	if not ":" in mac_addr:
		time.sleep(2)
		mac_addr = xbmc.getInfoLabel('Network.MacAddress')
        #print "MAC Adresa:%s"%mac_addr

	if ":" in mac_addr:
		return md5(str(mac_addr.decode("utf-8"))).hexdigest()
	else:
		return md5(str(uuid_node())).hexdigest()

def STATS(name, type):
    try:
        mac_address     = uniq_id(xbmc.getInfoLabel('Network.MacAddress'))
        addon_name      = __addon__.getAddonInfo('name')
        screen_width    = xbmc.getInfoLabel('System.ScreenWidth')
        screen_height   = xbmc.getInfoLabel('System.ScreenHeight')
        version_build   = xbmc.getInfoLabel('System.BuildVersion')
        version_kernel  = xbmc.getInfoLabel('System.KernelVersion')
        skin_name  = xbmc.getInfoLabel('Skin.CurrentTheme')
        mac_address     = uniq_id(xbmc.getInfoLabel('Network.MacAddress'))
        addon_name      = __addon__.getAddonInfo('name')
        screen_width    = xbmc.getInfoLabel('System.ScreenWidth')
        screen_height   = xbmc.getInfoLabel('System.ScreenHeight')
        version_build   = xbmc.getInfoLabel('System.BuildVersion')
        version_kernel  = xbmc.getInfoLabel('System.KernelVersion')
        skin_name  = xbmc.getInfoLabel('Skin.CurrentTheme')
        resolution = '%sx%s'%(screen_width, screen_height)
        
        url = 'http://kodi.extrapictures.cz/stats.php'
        url += '?userid=%s'%mac_address
        url += '&addon=%s'%addon_name
        url += '&resolution=%sx%s'%(screen_width, screen_height)
        url += '&version=%s'%version_build
        url += '&os=%s'%version_kernel
        url += '&skin=%s'%skin_name
        url += '&type=%s'%type #Item/Function
        url += '&name=%s'%name
        params = urllib.urlencode({'userid': mac_address, 'addon': addon_name, 'resolution': resolution, 'version': version_build, 'os': version_kernel, 'skin': skin_name, 'type': type, 'name': name})
        #con = urllib.urlopen("http://kodi.extrapictures.cz/stats.php?%s" % params)
        url = 'http://kodi.extrapictures.cz/stats.php?%s'%params.replace("+","%20")
        #print "Statistiky: %s"%url
        request = urllib2.Request(url)
        con = urllib2.urlopen(request)
        #data = con.read()
        con.close()
            
        #xbmcgui.Dialog().ok(addon_name, version_kernel, version_build,'%sx%s'%(screen_width, screen_height))
    except:
        print "Chyba zpracovani statistiky"