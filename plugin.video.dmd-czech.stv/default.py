# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
from urlparse import urlparse
import xbmcplugin,xbmcgui,xbmcaddon

_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.stv')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.stv')
__baseurl__ = 'http://www.rtvs.sk'
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

START_TOP= '<h2 class="nadpis">Najsledovanejšie</h2>'
END_TOP =  '<h2 class="nadpis">Najnovšie</h2>'
TOP_ITER_RE = '<li(.+?)<a title=\"(?P<title>[^"]+)\"(.+?)href=\"(?P<url>[^"]+)\"(.+?)<img src=\"(?P<img>[^"]+)\"(.+?)<p class=\"day\">(?P<date>[^<]+)<\/p>(.+?)<span class=\"programmeTime\">(?P<time>[^<]+)(.+?)<\/li>'

START_NEWEST = END_TOP
END_NEWEST = '<div class="footer'
NEWEST_ITER_RE = '<li(.+?)<a href=\"(?P<url>[^"]+)\"(.+?)title=\"(?P<title>[^"]+)\"(.+?)<img src=\"(?P<img>[^"]+)\"(.+?)<p class=\"day\">(?P<date>[^<]+)<\/p>(.+?)<span class=\"programmeTime\">(?P<time>[^<]+)(.+?)<\/li>'

START_AZ = '<h2 class="az"'
END_AZ = START_TOP
AZ_ITER_RE = TOP_ITER_RE

START_LISTING='<div class="boxRight archiv">'
END_LISTING='<div class="boxRight soloBtn white">'
LISTING_PAGER_RE= "<a class=\'prev calendarRoller' href=\'(?P<prevurl>[^\']+)\'.+?<a class=\'next calendarRoller\' href=\'(?P<nexturl>[^\']+)"
LISTING_DATE_RE = "<div class=\'calendar-header\'>\s+<h6>(?P<date>.+?)</h6>"
LISTING_ITER_RE = '<td class=(\"day\"|\"active day\")>\s+<a href="(?P<url>[^\"]+)\">(?P<daynum>[\d]+)</a>\s+</td>'

VIDEO_ID_RE = 'LiveboxPlayer.flash\(.+?stream_id:+.\"(.+?)\"'

def request(url,referer=None):
    request = urllib2.Request(url)
    request.add_header('User-Agent', _UserAgent_)
    if referer:
        request.add_header("Referer", url)
    response = urllib2.urlopen(request)
    data = response.read()
    response.close()
    return data

def substr(st,start=None,end=None):
    start_idx = start and st.find(start)
    start_idx = start_idx > -1 and start_idx or None
    end_idx = end and st.find(end)
    end_idx = end_idx > -1 and end_idx or None
    
    if start_idx and end_idx:
        return st[start_idx:end_idx]
    elif start_idx:
        return st[start_idx:]
    elif end_idx:
        return st[:end_idx]
    else: return st

def fix_url(url):
    return re.sub('&amp;','&',url)

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

def CATEGORIES():
    logo="http://www.rtvs.sk/images/logo-rtvs.png"
    addDir("Najsledovanejšie", __baseurl__ +'/tv.archive.alphabet', 1, logo)
    addDir("Najnovšie", __baseurl__ +'/tv.archive.alphabet', 2,logo)
    addDir("A-Z", __baseurl__ +'/tv.archive.alphabet', 3,icon)

def LIST_TOP(url):
    data = request(url)
    data = substr(data,START_TOP,END_TOP)
    for item in re.finditer(TOP_ITER_RE,data,re.IGNORECASE|re.DOTALL):
        title = item.group('title')
        date = item.group('date')
        time = item.group('time')
        link = __baseurl__+item.group('url')
        img = __baseurl__+item.group('img')
        addDir("%s (%s - %s)"%(title,date,time),link,10,img)

def LIST_NEWEST(url):
    data = request(url)
    data = substr(data,START_NEWEST,END_NEWEST)
    for item in re.finditer(NEWEST_ITER_RE,data,re.IGNORECASE|re.DOTALL):
        title = item.group('title')
        date = item.group('date')
        time = item.group('time')
        link = __baseurl__+item.group('url')
        img = __baseurl__+item.group('img')
        addDir("%s (%s - %s)"%(title,date,time),link,10,img)

def CATEGORY_AZ(url):
    az = [str(unichr(c)) for c in range(65,90,1)]
    for c in range(65,90,1):
        chr = str(unichr(c))
        addDir(chr,url+'?letter=%s'%chr.lower(),4,icon)

def LIST_AZ(url):
    data = request(url)
    data = substr(data,START_AZ,END_AZ)
    for item in re.finditer(AZ_ITER_RE,data,re.IGNORECASE|re.DOTALL):
        title = substr(item.group('title'),end=':').strip()
        link = __baseurl__+item.group('url')
        img = __baseurl__+item.group('img')
        addDir(title,link,5,img)

def LIST_TITLE(url):
    data = request(url)
    data = substr(data,START_LISTING,END_LISTING)
    current_date = re.search(LISTING_DATE_RE,data,re.IGNORECASE).group('date')
    prev_url = re.search(LISTING_PAGER_RE,data,re.IGNORECASE|re.DOTALL).group('prevurl')
    prev_url = fix_url(__baseurl__+prev_url)
    for item in re.finditer(LISTING_ITER_RE,data,re.IGNORECASE|re.DOTALL):
        title = "%s. %s"%(item.group('daynum'),current_date)
        link = fix_url(__baseurl__+item.group('url'))
        #img = __baseurl__+item.group('img')
        addDir(title,link,10,icon)
    addDir("<< Minulý mesiac",prev_url,5,nexticon)
    
def VIDEOLINK(url, name):
    httpdata = request(url)
    title = re.compile('<title>(.+?)</title>').findall(httpdata)
    title = title[0] + ' ' + name
    video_id = re.search(VIDEO_ID_RE, httpdata, re.IGNORECASE | re.DOTALL).group(1)
    keydata = request("http://embed.stv.livebox.sk/v1/tv-arch.js",referer=url)
    
    rtmp_url_regex="'(rtmp:\/\/[^']+)'\+videoID\+'([^']+)'"
    m3u8_url_regex="'(http:\/\/[^']+)'\+videoID\+'([^']+)'"
    rtmp = re.search(rtmp_url_regex,keydata,re.DOTALL)
    m3u8 = re.search(m3u8_url_regex,keydata,re.DOTALL)
    
    m3u8_url = m3u8.group(1) + video_id + m3u8.group(2)
    
    # rtmp[t][e|s]://hostname[:port][/app[/playpath]]
    # tcUrl=url URL of the target stream. Defaults to rtmp[t][e|s]://host[:port]/app. 
    
    # rtmp url- fix podla mponline2 projektu
    rtmp_url = rtmp.group(1)+video_id+rtmp.group(2)
    stream_part = 'mp4:'+video_id
    playpath = rtmp_url[rtmp_url.find(stream_part):]
    tcUrl = rtmp_url[:rtmp_url.find(stream_part)-1]+rtmp_url[rtmp_url.find(stream_part)+len(stream_part):]
    app = tcUrl[tcUrl.find('/',tcUrl.find('/')+2)+1:]

    #rtmp_url = rtmp_url+ ' playpath=' + playpath + ' tcUrl=' + tcUrl + ' app=' + app
    rtmp_url = rtmp_url+ ' tcUrl=' + tcUrl + ' app=' + app
    
    addLink(name+' [rtmp]', rtmp_url, icon, name)
    addLink(name+' [hls]', m3u8_url, icon, name)
    

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

print "stv: Mode: "+str(mode)
print "stv: URL: "+str(url)
print "stv: Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print "stv: "
        CATEGORIES()

elif mode == 1:
        print "stv: " + url
        LIST_TOP(url)
      
elif mode == 2:
        print "stv: " + url
        LIST_NEWEST(url)

elif mode == 3:
        print "stv: " + url
        CATEGORY_AZ(url)
        
elif mode == 4:
        print "stv: " + url
        LIST_AZ(url)

elif mode == 5:
        print "stv: " + url
        LIST_TITLE(url)

elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
