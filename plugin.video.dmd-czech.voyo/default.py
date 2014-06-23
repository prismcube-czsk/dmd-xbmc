# -*- coding: utf-8 -*-
import urllib2,urllib,re,os,string,time,base64,datetime
from urlparse import urlparse
try:
    import hashlib
except ImportError:
    import md5
import simplejson as json
import httplib
import requests

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
season_id = ''
if secret_token == '':
    xbmc.executebuiltin("XBMC.Notification('Doplněk DMD VOYO','Zadejte tajné heslo!',30000,"+icon+")")
    __settings__.openSettings() 
def OBSAH():
    addDir('Seriály','http://voyo.nova.cz/serialy/',5,icon,1)
    addDir('Pořady','http://voyo.nova.cz/porady/',5,icon,1)
    addDir('Zprávy','http://voyo.nova.cz/zpravy/',5,icon,1)
    addDir('Sport','http://voyo.nova.cz/sport/',5,icon,1)

    
def CATEGORIES_OLD(url,page):
    doc = read_page(url)
    items = doc.find('div', 'productsList series')
    print items
    for item in items.findAll('div', 'section_item'):
        if re.search('Přehrát', str(item), re.U):
                continue
        item2 = item.find('div', 'poster')    
        url = item2.a['href'].encode('utf-8')
        title = item2.a['title'].encode('utf-8')
        thumb = item2.a.img['src'].encode('utf-8')
        #print title,url,thumb
        addDir(title,__baseurl__+url,4,thumb)
    try:
        items = doc.find('div', 'pagination')
        dalsi = items.find('span', 'next next_page')
        if len(dalsi) != 0:
            next_url = str(dalsi.a['href']) 
        addDir('>> Další strana >>',__baseurl__+next_url,1,nexticon,1)
    except:
        print 'Stránkování nenalezeno'

def CATEGORIES(url,page):
    i = 0
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    section_id = re.compile('var ut_section_id = "(.+?)"').findall(httpdata)
    urlPath = urlparse(url)[2]
    try:
        match = re.compile('<div id="[0-9A-Za-z]+_productsListFoot">(.+?)Všechny seriály</p>', re.S).findall(httpdata)
        pageid = re.compile("'boxId': '(.+?)'", re.S).findall(str(match[0]))
        
    except:
        print "id nenalezeno"
    strquery = '?count=35&sectionId='+section_id[0]+'&showAs=2013&urlPath='+urlPath+'&resultType=categories&disablePagination=n&page='+str(page)+'&sortOrder=DESC&letterFilter=false'
    request = urllib2.Request(url, strquery)
    request.add_header("Referer",url)
    request.add_header("Host","voyo.nova.cz")
    request.add_header("Origin","http://voyo.nova.cz")
    request.add_header("X-Requested-With","XMLHttpRequest")
    request.add_header("User-Agent",_UserAgent_)
    request.add_header("Content-Type","application/x-www-form-urlencoded")
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    data = data.replace("<!doctype html>", "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
    doc = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    items = doc.find('div', 'productsList series')
    if items:
        for item in items.findAll('li', 'item_ul'):
            if re.search('Přehrát', str(item), re.U):
                continue
            item2 = item.find('div', 'poster')
            url2 = item2.a['href'].encode('utf-8')
            title = item2.a['title'].encode('utf-8')
            thumb = item2.a.img['src'].encode('utf-8')
            #print title,url,thumb
            i = i + 1
            addDir(title,__baseurl__+url2,2,thumb,1)
    else:
        items = doc.find('div', 'productList')
        for item in items.findAll('li', 'item'):
            url2 = item.a['href']
            thumb = item.a.img['src']
            title = item.findAll('a')[1].span.span.string.encode('utf-8')
            i = i + 1
            addDir(title,__baseurl__+url2,2,thumb,1)
    if i == 35:
        page = page + 1
        addDir('>> Další strana >>',url,5,nexticon,page)
        
def INDEX_OLD(url,page):
    doc = read_page(url)
    items = doc.find('div', 'productsList')
    for item in items.findAll('div', 'section_item'):
            item = item.find('div', 'poster')
            url = item.a['href'].encode('utf-8')
            title = item.a['title'].encode('utf-8')
            thumb = item.a.img['src'].encode('utf-8')
            print title,url,thumb
            addDir(title,__baseurl__+url,3,thumb,1)
    try:
        items = doc.find('div', 'pagination')
        for item in items.findAll('a'):
            page = item.text.encode('utf-8') 
            if re.match('další', page, re.U):
                next_url = item['href']
                #print next_url
                addDir('>> Další strana >>',__baseurl__+next_url,4,nexticon,1)                
    except:
        print 'strankovani nenalezeno'

def INDEX(url,page):
    season = None
    if '#' in url:
        season = url.split('#')[1]
        url = url.split('#')[0]
    vyjimka = ['/porady/30359-farma-epizody','/porady/30359-farma-nejnovejsi-dily','/porady/29930-farma-komentare-vypadnutych','/porady/29745-farma-cele-dily', '/porady/29564-farma-necenzurovane-dily', '/porady/29563-farma-deniky-soutezicich']
    i = 0
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    section_id = re.compile('var ut_section_id = "(.+?)"').findall(httpdata)
    product_id = re.compile('<input type="hidden" name="productId" value="(.+?)"').findall(httpdata)
    urlPath = urlparse(url)[2]
    try:
        match = re.compile('<div id="[0-9A-Za-z]+_productsListFoot">(.+?)Všechny seriály</p>', re.S).findall(httpdata)
        pageid = re.compile("'boxId': '(.+?)'", re.S).findall(str(match[0]))        
    except:
        print "strankovani nenalezeno"       
    strquery = '?count=35&sectionId='+section_id[0]+'&showAs=2013&urlPath='+urlPath+'&disablePagination=n&page='+str(page)+'&sortOrder=DESC&letterFilter=false'
    request = urllib2.Request(url, strquery)
    request.add_header("Referer",url)
    request.add_header("Host","voyo.nova.cz")
    request.add_header("Origin","http://voyo.nova.cz")
    request.add_header("X-Requested-With","XMLHttpRequest")
    request.add_header("User-Agent",_UserAgent_)
    request.add_header("Content-Type","application/x-www-form-urlencoded")
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()

    data = data.replace("<!doctype html>", "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">")
    doc = BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    if season:
        itemsEpisodeList = doc.findAll("div", {"id": "episodelist-"+season})
    else:
        itemsEpisodeList = doc.findAll("div", {"id": "episodelist-season-"})
    itemsMagicWrap = doc.find("div", {"id": "magic-wrap"})

    if itemsEpisodeList:
        for episode in itemsEpisodeList:
            thumb = episode.div.p.img['src']
            for item in reversed(episode.table.tbody.findAll('td')):
                if item.a:
                    url2 = item.a['href']
                    title = item.a['title'].encode('utf-8')
                    addDir(title,__baseurl__+url2,3,thumb,1)
    elif itemsMagicWrap:
        seasonSub = itemsMagicWrap.findAll('div', 'season-subgroups')
        for i in seasonSub:
            seasonSubP2 = i.find('li', 'season-sub p2')
            # Zjistim jestli je tam ta posrana lista s nabidkou
            if seasonSubP2:
                if '/' == seasonSubP2.a['href'][0]:
                    # Na strance jsou rovnou dily
                    myMode = 2
                else:
                    # Je tam lista
                    myMode = 6
                break
        for label in reversed(itemsMagicWrap.findAll('div', 'label')):
            # Vytahnu si nazvy adresaru a vytvorim je
            myUrl = url + label.a['href']
            season_id = label.a['href'].split('-')[1]
            addDir(label.a.text.encode('utf-8'),myUrl,myMode,'',1)


def JSON(url,page):
    if '#' in url:
        season = url.split('#')[1].split('-')[1]
    URL='voyo.nova.cz'
    
    conn = httplib.HTTPConnection(URL)
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        #'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '515',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'voyo.nova.cz',
        'Pragma': 'no-cache',
        'Referer': 'http://voyo.nova.cz/serialy/3919-ulice',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    body="allowTrialBadge=N&boxId=400051393d131248&count=50&chargeTypeFilter=yes&descrLength=100&itemDescriptionLength=100&disableFilter=n&disablePagination=n&enableRecommendations=n&expireBadge=N&genreId=&itemTpl=item_ul_v3.tpl&ignoreTreeOrderForEpisodes=n&letter=&letterFilter=n&page=1&productId=&parentId="+season+"&resultType=series&saveCount=0&setNewBadge=N&seriesFilter=n&sectionId=69003&showAs=2013&showInTv=n&sort=id&sortOrder=ASC&subsiteId=503&templateType=json&templateFileItem=item_ul_v3.tpl&toggleSortOrder=0&version=3"
    
    conn.request('POST', '/bin/eshop/product/filter.php', body=body, headers=header)
    res = conn.getresponse()
    httpdata = res.read()
    conn.close()
    jsondata = json.loads(httpdata)
    for d in reversed(jsondata["result"]):
        addDir(d["title"].encode('utf-8'),"http://" + URL + d["href"],2,'',1)

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
            addLink('HQ '+name,rtmp_url_hq,icon,desc)
        elif __settings__.getSetting('kvalita_sel') == "LQ":
            addLink('LQ '+name,rtmp_url_lq,icon,desc)
        elif __settings__.getSetting('kvalita_sel') == "HD":
            if rtmp_url_hd == 0:
                addLink('HQ '+name,rtmp_url_hq,icon,desc)                
            else:
                addLink('HD '+name,rtmp_url_hd,icon,desc)
        else:
            addLink('HQ '+name,rtmp_url_hq,icon,desc)                


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
        OBSAH()

elif mode==1:
        print ""+url
        print ""+str(page)                
        CATEGORIES_OLD(url,page)
elif mode==5:
        print ""+url
        print ""+str(page)        
        CATEGORIES(url,page)
     
       
elif mode==2:
        print ""+url
        print ""+str(page)        
        INDEX(url,page)
elif mode==4:
        print ""+url
        print ""+str(page)                
        INDEX_OLD(url,page)        

elif mode==3:
        print ""+url
        try:
            VIDEOLINK(url, name)
        except IndexError:
            INDEX(url, name)

elif mode==6:
    print ""+url
    print ""+str(page)
    JSON(url,page)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
