# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
__baseurl__ = 'http://www.iprima.cz/videoarchiv'
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
file = __settings__.getSetting('xml_file')

def replace_words(text, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)

word_dic = {
'\u00e1': 'á',
'\u00e9': 'é',
'\u00ed': 'í',
'\u00fd': 'ý',
'\u00f3': 'ó',
'\u00fa': 'ú',
'\u016f': 'ů',
'\u011b': 'ě',
'\u0161': 'š',
'\u0165': 'ť',
'\u010d': 'č',
'\u0159': 'ř',
'\u017e': 'ž',
'\u010f': 'ď',
'\u0148': 'ň',
'\u00C0': 'Á',
'\u00c9': 'É',
'\u00cd': 'Í',
'\u00d3': 'Ó',
'\u00da': 'Ú',
'\u016e': 'Ů',
'\u0115': 'Ě',
'\u0160': 'Š',
'\u010c': 'Č',
'\u0158': 'Ř',
'\u0164': 'Ť',
'\u017d': 'Ž',
'\u010e': 'Ď',
'\u0147': 'Ň'
}


def CATEGORIES():
    req = urllib2.Request(__baseurl__)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<div class="field-content"><a href="/videoarchiv/(.+?)" class="modalframe-exclude">(.+?)</a></div>').findall(httpdata)

    for url,name in match:
        thumb = re.compile('([0-9]+)').findall(url)
        addDir(name,'http://www.iprima.cz/videoarchiv_ajax/'+url,1,__dmdbase__+thumb[0]+'.jpg',0)
        
def INDEX(url,page):
    # parametry pro skript
    if int(page) != 0:
        strquery = '?method=json&action=relevant&page='+str(page)
    else:
        strquery = '?method=json&action=relevant'
    print strquery    
    doc = read_page(url+strquery)
    match = re.compile('"nid":"(.+?)","title":"(.+?)","date":"(.+?)","view_count":.+?,"comment_count":".+?","image":".+?/(.+?)"').findall(str(doc))
    for videoid,name,datum,thumb in match:
            name = replace_words(name, word_dic)
            thumb = replace_words(thumb, word_dic)
            #print str(name),'http://www.iprima.cz/videoarchiv_ajax/'+videoid,2,'http://www.iprima.cz/sites/'+thumb
            addDir(str(name),'http://www.iprima.cz/videoarchiv/'+videoid+'/',2,'http://www.iprima.cz/sites/'+thumb,'')

    strankovani = re.compile('"total":(.+?),"from":.+?,"to":.+?,"page":(.+?),').findall(str(doc))
    for page_total,act_page in strankovani:
        print page_total,act_page
        if int(page_total) > 10:
            act_page = act_page.replace('"','')
            next_page = int(act_page)  + 1
            max_page =  round(int(page_total)/10,0 )
            if next_page < max_page+1:
                max_page = str(max_page+1)
                max_page = re.sub('.0','',max_page)
                #print '>> Další strana >>',url,1,next_page
                addDir('>> Další strana ('+str(next_page+1)+' z '+max_page+')',url,1,nexticon,next_page)
        
def VIDEOLINK(url,name):
    # parametry pro skript
    strquery = '?method=json&action=video'
    # pozadavek na skript
    request = urllib2.Request(url, strquery)
    con = urllib2.urlopen(request)
    # nacteni stranky
    data = con.read()
    con.close()
    # naplneni promenne obsahem stranky
    print url
    stream_video = re.compile('cdnID=([0-9]+)').findall(data)
    if len(stream_video) > 0:
        print 'LQ '+__cdn_url__+name,stream_video[0],icon,''
        addLink('LQ '+name,__cdn_url__+stream_video[0],icon,'')        
    else:
        livebox = re.compile("'512','414', '(.+?)', '(.+?)', '(.+?)'").findall(data)
        #hq_stream = livebox[0]
        #lq_stream = livebox[1]
        #thumb = livebox[2]
        for hq_stream,lq_stream,thumb in livebox:
            nahled = 'http://embed.livebox.cz/iprima/'+thumb
            hq_url = 'rtmp://iprima.livebox.cz/iprima/'+hq_stream                
            lq_url = 'rtmp://iprima.livebox.cz/iprima/'+lq_stream                
            print nahled, hq_url, lq_url
            if __settings__.getSetting('kvalita_sel') == "true":
                print 'HQ '+name,hq_url,nahled,name
                addLink('HQ '+name,hq_url,nahled,name)
            if __settings__.getSetting('kvalita_sel') == "false":
                print 'LQ '+name,lq_url,nahled,name
                addLink('LQ '+name,lq_url,nahled,name)


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

def addDir(name,url,mode,iconimage,page):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)
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
page=None
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
try:
        page=int(params["page"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Page: "+str(page)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        print ""+str(page)
        INDEX(url,page)
        
elif mode==2:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
