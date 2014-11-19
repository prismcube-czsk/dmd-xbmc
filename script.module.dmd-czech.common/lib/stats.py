# -*- coding: utf-8 -*-

import xbmc, xbmcgui, xbmcaddon, time, datetime
import urllib, urllib2, re
from hashlib import md5
import threading

__addon__       = xbmcaddon.Addon()
__addon2__       = xbmcaddon.Addon('script.module.dmd-czech.common')
_UserAgent_     = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
busystring = xbmc.getLocalizedString(503).encode("utf8")


def GET_MAC():
    #Ulozeni MAC
    mac_settings = __addon2__.getSetting('mac')
    if mac_settings == "":   
        mac_address = xbmc.getInfoLabel('Network.MacAddress')
        i = 1
        while mac_address == busystring:
            print "cekam: %s"%i
            i = i+1
            mac_address = xbmc.getInfoLabel('Network.MacAddress') 
            time.sleep(1)
            if i == 10:
                break
        timestamp       = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
        __addon2__.setSetting('mac', mac_address)
        __addon2__.setSetting('timestamp', timestamp)
        
def GET_OS():
    #Ulozeni OS
    kernel_settings = __addon2__.getSetting('kernel_version')
    if kernel_settings == "":   
        kernel_version = xbmc.getInfoLabel('System.KernelVersion')
        i = 1
        while kernel_version == busystring:
            print "cekam: %s"%i
            i = i+1
            kernel_version = xbmc.getInfoLabel('System.KernelVersion') 
            time.sleep(1)
            if i == 10:
                break
        timestamp       = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
        __addon2__.setSetting('kernel_version', kernel_version)
        __addon2__.setSetting('timestamp', timestamp)

def REFRESH():
    time_settings = datetime.datetime.fromtimestamp(time.mktime(time.strptime(__addon2__.getSetting('timestamp'), '%Y-%m-%d %H:%M:%S')))
    if time_settings < datetime.datetime.now()-datetime.timedelta(days=7):
        __addon2__.setSetting('mac', "")
        __addon2__.setSetting('kernel_version', "")
        __addon2__.setSetting('timestamp', "")
        


def SEND_STATS(name, type):
    GET_MAC()
    GET_OS()      
    if __addon2__.getSetting('mac') != busystring:
        try:
            mac_address     = md5(str(__addon2__.getSetting('mac').decode("utf-8"))).hexdigest()
            addon_name      = __addon__.getAddonInfo('name')
            screen_width    = xbmc.getInfoLabel('System.ScreenWidth')
            screen_height   = xbmc.getInfoLabel('System.ScreenHeight')
            version_build   = xbmc.getInfoLabel('System.BuildVersion')
            version_kernel  = __addon2__.getSetting('kernel_version')
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
            httpdata = con.read()
            con.close()
            #print "odesilam statistiky"
            #xbmcgui.Dialog().ok(addon_name, version_kernel, version_build,'%sx%s'%(screen_width, screen_height))
        except:
            print "Chyba zpracovani statistiky"
        REFRESH()
   
        try:
            news_time_settings = datetime.datetime.fromtimestamp(time.mktime(time.strptime(__addon2__.getSetting('timestamp_news'), '%Y-%m-%d %H:%M:%S')))
        except:
            news_time_settings = datetime.datetime.fromtimestamp(time.mktime(time.strptime('2000-10-10 10:10:10', '%Y-%m-%d %H:%M:%S')))
        
        try:
            match = re.compile('<timestamp>(.+?)</timestamp>').findall(httpdata)
            news_timestamp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(match[0], '%Y-%m-%d %H:%M:%S')))
            if news_time_settings < news_timestamp:
                match = re.compile('<title>(.+?)</title>').findall(httpdata)
                news_title = match[0]
                match = re.compile('<line1>(.+?)</line1>').findall(httpdata)
                news_line1 = match[0]
                match = re.compile('<line2>(.+?)</line2>').findall(httpdata)
                news_line2 = match[0]
                match = re.compile('<line3>(.+?)</line3>').findall(httpdata)
                news_line3 = match[0]
                __addon2__.setSetting('timestamp_news', news_timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                xbmcgui.Dialog().ok(news_title, news_line1, news_line2,news_line3)
        except:
            print "Chyba načtení novinek"
def STATS(name, item_type):
	try:
		t = threading.Thread(target=SEND_STATS, args = (name, item_type))
		t.daemon = True
		t.start()
	except:
		pass