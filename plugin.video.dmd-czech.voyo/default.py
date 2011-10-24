# -*- coding: utf-8 -*-
import urllib2,urllib,re,os,string,time,base64,md5,datetime
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://voyo.nova.cz'
__dmdbase__ = 'http://iamm.uvadi.cz/xbmc/voyo/'
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.voyo')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.voyo')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
page_pole_url = []
page_pole_no = []
secret_token =__settings__.getSetting('secret_token')
#rtmp_token =__settings__.getSetting('rtmp_token')
nova_service_url = 'http://master-ng.nacevi.cz/cdn.server/PlayerLink.ashx'
nova_app_id = 'nova-vod'
if secret_token == '':
    xbmc.executebuiltin("XBMC.Notification('Doplněk DMD VOYO','Zadejte tajné heslo!',30000,"+icon+")")
    __settings__.openSettings() 
def CATEGORIES():
    zakazane = ['zenaty-se-zavazky', 'tudorovci', 'kobra-11', 'patty-hewes', 'policejni-odznak']
    req = urllib2.Request(__baseurl__)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<a class="list_item" href="/(.+?)/">(.+?)</a>').findall(httpdata)
    for url,name in match:
        if url in zakazane:
            continue        
        addDir(name,__baseurl__+'/'+url+'/',1,__dmdbase__+url+'.jpg')
        
def INDEX(url):
    doc = read_page(url)
    items = doc.find('div', id='searched_videos')
    for item in items.findAll('li', 'catchup_related_video status_'):
            name_a = item.find('strong', 'info_title')
            name = name_a.getText(" ").encode('utf-8')
            url = __baseurl__+str(item.a['href'])
            datum_a = item.find('span', 'date')
            datum = datum_a.getText(" ")
            thumb = str(item.a.img['src'])            
            #print name, thumb, url, datum, plot
            addDir(name,url,2,thumb)
    try:
        pager = doc.find('div', id='pager')
        act_page_a = pager.find('span', 'selected ')
        act_page = act_page_a.getText(" ").encode('utf-8')
        next_page = int(act_page) + 1
        url_page = int(act_page)-1
        #print act_page, url_page
        for item in pager.findAll('a'):
            page_url = item['href'].encode('utf-8')
            page_no = item.getText(" ").encode('utf-8')
            #print page_url,page_no
            page_pole_url.append(page_url)
            page_pole_no.append(page_no)
        max_page_count = len(page_pole_no)-1
        next_url = page_pole_url[url_page]
        max_page = page_pole_no[max_page_count]
        next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
        addDir(next_label,__baseurl__+next_url,1,nexticon)
    except:
        print 'stop'
        
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    mediaid = re.compile('media_id = "(.+?)"').findall(httpdata)
    thumb = re.compile('<link rel="image_src" href="(.+?)" />').findall(httpdata)
    popis = re.compile('<meta name="description" content="(.+?)" />').findall(httpdata)
    datum = datetime.datetime.now()
    timestamp = datum.strftime('%Y%m%d%H%M%S')
    videoid = urllib.quote(nova_app_id + '|' + mediaid[0])
    md5hash = nova_app_id + '|' + mediaid[0] + '|' + timestamp + '|' + secret_token
    md5hash = md5.new(md5hash)
    signature = urllib.quote(base64.b64encode(md5hash.digest()))
    config = nova_service_url + '?t=' + timestamp + '&d=1&tm=nova&h=0&c=' +videoid+ '&s='+signature    
    print config
    try:
        desc = popis[0]
    except:
        desc = name
    req = urllib2.Request(config)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    error_secret_token = re.compile('<errorCode>(.+?)</errorCode>').findall(httpdata)
    try:
        chyba = int(error_secret_token[0])
    except:
        chyba = 0
    if chyba == 2:    
        print 'Nesprávné tajné heslo'
        xbmc.executebuiltin("XBMC.Notification('Doplněk DMD VOYO','Nesprávné tajné heslo!',30000,"+icon+")")
        __settings__.openSettings()        
    elif chyba == 1:    
        print 'Špatné časové razítko'
        xbmc.executebuiltin("XBMC.Notification('Doplněk DMD VOYO','Nesprávné časové razítko!',30000,"+icon+")")      
    elif chyba == 0:
        baseurl = re.compile('<baseUrl>(.+?)</baseUrl>').findall(httpdata)
        streamurl = re.compile('<url>(.+?)</url>').findall(httpdata)
        urllq = streamurl[0].encode('utf-8')
        urlhq = streamurl[1].encode('utf-8')
        swfurl = 'http://voyo.nova.cz/static/shared/app/flowplayer/13-flowplayer.commercial-3.1.5-19-003.swf'
        #rtmp_url_lq = baseurl[0]+' playpath='+urllq+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true token='+rtmp_token 
        rtmp_url_lq = baseurl[0]+' playpath='+urllq
        #rtmp_url_hq = baseurl[0]+' playpath='+urlhq+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true token='+rtmp_token 
        rtmp_url_hq = baseurl[0]+' playpath='+urlhq
        if __settings__.getSetting('kvalita_sel') == "true":
            addLink(name,rtmp_url_hq,thumb[0],desc)
        if __settings__.getSetting('kvalita_sel') == "false":
            addLink(name,rtmp_url_lq,thumb[0],desc)


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
