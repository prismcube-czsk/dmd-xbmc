# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import time
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__='http://www.iprima.cz/showjanakrause/videoarchiv'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.sjk')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.sjk')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
file = __settings__.getSetting('xml_file')

def OBSAH():
    #self.core.setSorting('NONE')
    req = urllib2.Request(__baseurl__)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<a href="(.+?)">(.+?)</a>.*?</td>').findall(httpdata)
    counter = 0
    count = len(match)/2
    for url,name in match:
        name = name.replace('<strong>','')
        name = name.replace('</strong>','')
        name = name.capitalize()
        counter += 1
        #print 'Show Jana Krause '+name,url
        if counter<=count:
            addDir('Show Jana Krause '+name,url,1,icon)    

            
def INDEX(url):
    #self.core.setSorting('NONE')
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile("'295','183', '(.+?)', '(.+?)','(.+?)','(.+?)'").findall(httpdata)
    for hq_stream,lq_stream,thumb,datum in match:
        ts = time.strptime(datum[:19], "%Y/%m/%d %H:%M:%S")
        day_string = time.strftime("%d.%m.%Y", ts)
        if re.match('KrausCut', hq_stream, re.U):
                name = 'Vystřižené scény z natáčení '+day_string
                #print hq_stream,lq_stream,thumb,'Vystřižené scény z natáčení '+day_string        
        if not re.match('KrausCut', hq_stream, re.U):
                name = 'Show Jana Krause '+day_string
                #print hq_stream,lq_stream,thumb,'Show Jana Krause '+day_string
        nahled = 'http://embed.livebox.cz/iprima/'+thumb
        hq_url = 'rtmp://iprima.livebox.cz/iprima/'+hq_stream                
        lq_url = 'rtmp://iprima.livebox.cz/iprima/'+lq_stream                
        if __settings__.getSetting('kvalita_sel') == "true":
            addLink('HQ '+name,hq_url,nahled,name)
        if __settings__.getSetting('kvalita_sel') == "false":
            addLink('LQ '+name,hq_url,nahled,name)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param



def addLink(name,url,iconimage,popis):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": popis} )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
params=get_params()
url=None
name=None
thumb=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        OBSAH()
       
elif mode==1:
        print ""
        INDEX(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
