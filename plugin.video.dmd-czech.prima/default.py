# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://prima.stream.cz'
__cdn_url__  = 'http://cdn-dispatcher.stream.cz/?id='
__dmdbase__ = 'http://iamm.uvadi.cz/xbmc/prima/'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.prima')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.prima')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
page_pole_url = []
page_pole_no = []


def CATEGORIES():
    #addDir('112','http://voyo.nova.cz/112/',1,'http://iamm.netuje.cz/emulator/voyo/image/112.jpg')
    #addDir( 'Babicovy dobroty','http://voyo.nova.cz/babicovy-dobroty/',1,'http://iamm.netuje.cz/emulator/voyo/image/babicovy-dobroty.jpg')
    #self.core.setSorting('NONE')
    req = urllib2.Request(__baseurl__)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<li><a href="http://prima.stream.cz/(.+?)/">(.+?)</a></li>').findall(httpdata)

    for url,name in match:
        addDir(name,__baseurl__+'/'+url+'/',1,__dmdbase__+url+'.jpg')
        
def INDEX(url):
    doc = read_page(url)
    items = doc.find('div', id='videa_kanalu_list')
    for item in items.findAll('div', 'kanal_1video'):
            thumb = item.find('a', 'kanal_1video_pic')
            thumb = thumb['style']
            thumb = thumb[(thumb.find('url(') + len('url(') + 1):] 
            thumb = thumb[:(thumb.find(')') - 1)]
            name_a = item.find('a', 'kanal_1video_title')
            name = name_a.getText(" ").encode('utf-8')
            url = str(item.a['href'])
            plot = item.find('div', 'kanal_1video_text')
            plot = plot.getText(" ").encode('utf-8')
            #print name, thumb, url, datum, plot
            addDir(name,url,2,thumb)
    try:
        items = doc.find('div', 'paging')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('další', page, re.U):
                next_url = item['href']
                #print 'Další strana',item['href']
                addDir('Další strana',__baseurl__+next_url,1,nexticon)
        
    except:
        print 'strankovani nenalezeno'
        
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    try:
        hd_video = re.compile('cdnHD=([0-9]+)').findall(httpdata)
    except:
        print 'HD stream nenalezen'
    try:
        hq_video = re.compile('cdnHQ=([0-9]+)').findall(httpdata)
    except:
        print 'HD stream nenalezen'
    try:
        lq_video = re.compile('cdnLQ=([0-9]+)').findall(httpdata)
    except:
        print 'LQ stream nenalezen'
    thumb = re.compile('<link rel="image_src" href="(.+?)" />').findall(httpdata)
    popis = re.compile('<meta name="title" content="(.+?) - Video na Stream.cz" />').findall(httpdata)
    #print name,urlhq,thumb
    if len(hd_video)>0:
        hdurl = __cdn_url__ + hd_video[0]
        #print 'HD '+'name',hdurl,popis[0]
        addLink('HD '+name,hdurl,'',popis[0])
    if len(hq_video)>0:
        hqurl = __cdn_url__ + hq_video[0]
        #print 'HQ '+'name',hqurl,'',popis[0]
        addLink('HQ '+name,hqurl,'',popis[0])
    if len(lq_video)>0:
        lqurl = __cdn_url__ + lq_video[0]
        #print'LQ '+'name',lqurl,'',popis[0]
        addLink('LQ '+name,lqurl,'',popis[0])        
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
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
