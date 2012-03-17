# -*- coding: utf-8 -*-
import urllib2,urllib,re,os,string,time,base64,datetime
try:
    import hashlib
except ImportError:
    import md5

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
rtmp_token = 'h0M*t:pa$kA'
nova_service_url = 'http://master-ng.nacevi.cz/cdn.server/PlayerLink.ashx'
nova_app_id = 'nova-vod'
if secret_token == '':
    xbmc.executebuiltin("XBMC.Notification('Doplněk DMD VOYO','Zadejte tajné heslo!',30000,"+icon+")")
    __settings__.openSettings() 
def OBSAH():
    addDir('Seriály','http://voyo.nova.cz/serialy/',1,icon)
    addDir('Pořady','http://voyo.nova.cz/porady/',1,icon)
    addDir('Zprávy','http://voyo.nova.cz/zpravy/',1,icon)
    
def CATEGORIES(url):
    zakazane = ['/tvod/serialy/27522-zvire', '/serialy/27540-powder-park', '/serialy/27483-osklive-kacatko-a-ja','/serialy/26481-odvazny-crusoe','/serialy/26482-5-dnu-do-pulnoci','/serialy/3924-patty-hewes','/serialy/27216-lazytown','/serialy/3923-tudorovci','/serialy/3906-kobra-11']
    pole_poradu = 0
    doc = read_page(url)
    for porady in doc.findAll('div', 'productsList'):
            pole_poradu = pole_poradu + 1        
            if pole_poradu == 1:
                continue
            for item in porady.findAll('div', 'section_item'):
                item = item.find('div', 'poster')
                url = item.a['href'].encode('utf-8')
                title = item.a['title'].encode('utf-8')
                thumb = item.a.img['src'].encode('utf-8')
                #print title,url,thumb
                if url in zakazane:
                    continue
                addDir(title,__baseurl__+url,2,thumb)
    try:
        items = doc.find('div', 'pagination')
        for item in items.findAll('span', 'normal'):
            url = __baseurl__+str(item.a['href'])
            doc = read_page(url)
            pole_poradu = 0
            for porady in doc.findAll('div', 'productsList'):
                pole_poradu = pole_poradu + 1        
                if pole_poradu == 1:
                    continue
                for item in porady.findAll('div', 'section_item'):
                    item = item.find('div', 'poster')
                    url = item.a['href'].encode('utf-8')
                    title = item.a['title'].encode('utf-8')
                    thumb = item.a.img['src'].encode('utf-8')
                    #print title,url,thumb
                    if url in zakazane:
                        continue
                    addDir(title,__baseurl__+url,2,thumb)
    except:
        print 'Stránkování nenalezeno'

        
def INDEX(url):
    doc = read_page(url)
    items = doc.find('div', 'productsList')
    for item in items.findAll('div', 'section_item'):
            item = item.find('div', 'poster')
            url = item.a['href'].encode('utf-8')
            title = item.a['title'].encode('utf-8')
            thumb = item.a.img['src'].encode('utf-8')
            if __settings__.getSetting('test_nastaveni') == "true":
                print title,url,thumb
            addDir(title,__baseurl__+url,3,thumb)
    try:
        items = doc.find('div', 'pagination')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('další', page, re.U):
                next_url = item['href']
                #print next_url
                addDir('>> Další strana >>',__baseurl__+next_url,2,nexticon)                
    except:
        print 'strankovani nenalezeno'
        
def VIDEOLINK(url,name):
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    mediaid = re.compile('mainVideo = new mediaData\(.+?, .+?, (.+?),').findall(httpdata)
    thumb = re.compile('<link rel="image_src" href="(.+?)" />').findall(httpdata)
    popis = re.compile('<meta name="description" content="(.+?)" />').findall(httpdata)
    datum = datetime.datetime.now()
    timestamp = datum.strftime('%Y%m%d%H%M%S')
    videoid = urllib.quote(nova_app_id + '|' + mediaid[0])
    md5hash = nova_app_id + '|' + mediaid[0] + '|' + timestamp + '|' + secret_token
    try:
        md5hash = hashlib.md5(md5hash)
    except:
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
    if __settings__.getSetting('test_nastaveni') == "true":
        print httpdata
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
        xbmc.executebuiltin("XBMC.Notification('Doplněk DMD VOYO','Pořad lze přehrát pouze na webu Voyo.cz!',30000,"+icon+")")      
    elif chyba == 0:
        baseurl = re.compile('<baseUrl>(.+?)</baseUrl>').findall(httpdata)
        streamurl = re.compile('<media>\s<quality>(.+?)</quality>.\s<url>(.+?)</url>\s</media>').findall(httpdata)        
        for kvalita,odkaz in streamurl:
            #print kvalita,odkaz
            if re.match('hd', kvalita, re.U):
                urlhd = odkaz.encode('utf-8')
            elif re.match('hq', kvalita, re.U):
                urlhq = odkaz.encode('utf-8')
            elif re.match('lq', kvalita, re.U):
                urllq = odkaz.encode('utf-8')
        print urlhq,urllq
        swfurl = 'http://voyo.nova.cz/static/shared/app/flowplayer/13-flowplayer.commercial-3.1.5-19-003.swf'
        if __settings__.getSetting('test_nastaveni') == "true":          
            rtmp_url_lq = baseurl[0]+' playpath='+urllq+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true token='+rtmp_token 
            rtmp_url_hq = baseurl[0]+' playpath='+urlhq+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true token='+rtmp_token 
            try:
                rtmp_url_hd = baseurl[0]+' playpath='+urlhd+' pageUrl='+url+' swfUrl='+swfurl+' swfVfy=true token='+rtmp_token 
            except:
                rtmp_url_hd = 0
        else:
            rtmp_url_lq = baseurl[0]+' playpath='+urllq
            rtmp_url_hq = baseurl[0]+' playpath='+urlhq
            try:
                rtmp_url_hd = baseurl[0]+' playpath='+urlhd            
            except:
                rtmp_url_hd = 0
        if __settings__.getSetting('kvalita_sel') == "HQ":
            addLink(name,rtmp_url_hq,icon,desc)
        elif __settings__.getSetting('kvalita_sel') == "LQ":
            addLink(name,rtmp_url_lq,icon,desc)
        elif __settings__.getSetting('kvalita_sel') == "HD":
            if rtmp_url_hd == 0:
                addLink(name,rtmp_url_hq,icon,desc)                
            else:
                addLink(name,rtmp_url_hd,icon,desc)
        else:
            addLink(name,rtmp_url_hq,icon,desc)                


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
        print ""+url
        CATEGORIES(url)
       
elif mode==2:
        print ""+url
        INDEX(url)
elif mode==4:
        print ""+url
        FILMY(url)
        
elif mode==3:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
