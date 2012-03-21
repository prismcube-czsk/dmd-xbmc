# -*- coding: utf-8 -*-
import urllib2,urllib,re,os,random,decimal
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
family = xbmc.translatePath( os.path.join( home, 'family.png' ) )
love = xbmc.translatePath( os.path.join( home, 'love.png' ) )
cool = xbmc.translatePath( os.path.join( home, 'cool.png' ) )
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

def OBSAH():
    addDir('Family','http://play.iprima.cz/',1,family,'','')
    addDir('Love','http://play.iprima.cz/',2,love,'','')
    addDir('COOL','http://play.iprima.cz/',3,cool,'','')
    
def OBSAH_FAMILY(url):
    addDir('Aféry','9415',4,__dmdbase__+'9415.jpg',0,1)
    addDir('Ano,šéfe!','2290',4,__dmdbase__+'2290.jpg',0,1)
    addDir('Aréna národů','15727',4,__dmdbase__+'15727.jpg',0,1)
    addDir('Autosalon','2288',4,__dmdbase__+'2288.jpg',0,1)    
    addDir('Bubo bubo','13037',4,__dmdbase__+'13037.jpg',0,1)
    addDir('Cesty domů','6840',4,__dmdbase__+'6840.jpg',0,1)
    addDir('Fakta Brabory Techecí','3976',4,__dmdbase__+'3976.jpg',0,1)
    addDir('Farmář hledá ženu','6130',4,__dmdbase__+'6130.jpg',0,1)
    addDir('Filmy','15151',4,__dmdbase__+'15151.jpg',0,1)
    addDir('Hotel Paradise','16268',4,__dmdbase__+'16268.jpg',0,1)    
    addDir('Hotel Paradise - Videospeciál','16369',4,__dmdbase__+'16369.jpg',0,1)    
    addDir('Jak se staví dům','2291',4,__dmdbase__+'2291.jpg',0,1)
    addDir('Jak se staví sen','1187',4,__dmdbase__+'1187.jpg',0,1)
    addDir('Jste to co jíte','2287',4,__dmdbase__+'2287.jpg',0,1)
    addDir('Krimi zprávy','3773',4,__dmdbase__+'3773.jpg',0,1)
    addDir('Letiště','2297',4,__dmdbase__+'2297.jpg',0,1)
    addDir('Moje místo','13347',4,__dmdbase__+'13347.jpg',0,1)
    addDir('Máš minutu','9900',4,__dmdbase__+'9900.jpg',0,1)
    addDir('Nemocnice XXXXL','16200',4,__dmdbase__+'16200.jpg',0,1)
    addDir('Nikdo není dokonalý speciál','6548',4,__dmdbase__+'6548.jpg',0,1)
    addDir('Nové hnízdo','12732',4,__dmdbase__+'12732.jpg',0,1)
    addDir('O mé rodině a ...','13583',4,__dmdbase__+'13583.jpg',0,1)
    addDir('Partie','1185',4,__dmdbase__+'1185.jpg',0,1)
    addDir('Partička','9416',4,__dmdbase__+'9416.jpg',0,1)
    addDir('Partička speciály','14104',4,__dmdbase__+'14104.jpg',0,1)
    addDir('Prima tip na večeři','2295',4,__dmdbase__+'2295.jpg',0,1)
    addDir('Prostřeno!','4114',4,__dmdbase__+'4114.jpg',0,1)
    addDir('Přešlapy','2494',4,__dmdbase__+'2494.jpg',0,1)
    addDir('Receptář Prima nápadů','2501',4,__dmdbase__+'2501.jpg',0,1)
    addDir('S italem v kuchyni','2544',4,__dmdbase__+'2544.jpg',0,1)
    addDir('Show Jana Krause','6577',4,__dmdbase__+'6577.jpg',0,1)
    addDir('Skečbar','7099',4,__dmdbase__+'7099.jpg',0,1)
    addDir('Soukromá dramata','6550',4,__dmdbase__+'6550.jpg',0,1)
    addDir('Top Star Magazín','1184',4,__dmdbase__+'1184.jpg',0,1)
    addDir('VIP Prostřeno!','15291',4,__dmdbase__+'15291.jpg',0,1)
    addDir('VIP zprávy','6037',4,__dmdbase__+'6037.jpg',0,1)
    addDir('Velmi křehké vztahy','2283',4,__dmdbase__+'2283.jpg',0,1)
    addDir('Vrabci v hrsti','11980',4,__dmdbase__+'11980.jpg',0,1)
    addDir('Vraždy v Midsomeru','15977',4,__dmdbase__+'15977.jpg',0,1)
    addDir('Vánoční pečení','14878',4,__dmdbase__+'14878.jpg',0,1)
    addDir('Zprávy FTV Prima','2317',4,__dmdbase__+'2317.jpg',0,1)
    addDir('Zázraky Života','4288',4,__dmdbase__+'4288.jpg',0,1)
    addDir('Česko na talíři','14020',4,__dmdbase__+'14020.jpg',0,1)
    addDir('Čápi s mákem','6547',4,__dmdbase__+'6547.jpg',0,1)
    addDir('Šéf na grilu','10728',4,__dmdbase__+'10728.jpg',0,1)
    addDir('Ženy na cestách','15610',4,__dmdbase__+'15610.jpg',0,1)
    addDir('Životní úklid','14019',4,__dmdbase__+'14019.jpg',0,1)

def OBSAH_LOVE(url):
    addDir('Aféry','9415',4,__dmdbase__+'9415.jpg',0,3)
    addDir('Eliso, vrať se!','14521',4,__dmdbase__+'14521.jpg',0,3)
    addDir('Farmář hledá ženu','6130',4,__dmdbase__+'6130.jpg',0,3)
    addDir('Filmy','15151',4,__dmdbase__+'15151.jpg',0,3)
    addDir('Hotel Paradise','16268',4,__dmdbase__+'16268.jpg',0,3)    
    addDir('Hotel Paradise - Videospeciál','16369',4,__dmdbase__+'16369.jpg',0,3)    
    addDir('Hříšná láska','16118',4,__dmdbase__+'16118.jpg',0,3)
    addDir('Jak se staví dům','2291',4,__dmdbase__+'2291.jpg',0,3)
    addDir('Jak se staví sen','1187',4,__dmdbase__+'1187.jpg',0,3)
    addDir('Jste to co jíte','2287',4,__dmdbase__+'2287.jpg',0,3)
    addDir('Letiště','2297',4,__dmdbase__+'2297.jpg',0,3)
    addDir('Nemocnice XXXXL','16200',4,__dmdbase__+'16200.jpg',0,3)
    addDir('Přešlapy','2494',4,__dmdbase__+'2494.jpg',0,3)
    addDir('S italem v kuchyni','2544',4,__dmdbase__+'2544.jpg',0,3)
    addDir('Top Star LOVE','16465',4,__dmdbase__+'16465.jpg',0,3)
    addDir('Top Star Magazín','1184',4,__dmdbase__+'1184.jpg',0,3)
    addDir('Tráva','14879',4,__dmdbase__+'14879.jpg',0,3)

def OBSAH_COOL(url):
    addDir('Autosalon','2288',4,__dmdbase__+'2288.jpg',0,2)
    addDir('Filmy','15151',4,__dmdbase__+'15151.jpg',0,2)
    addDir('Misfits: Zmetci','16103',4,__dmdbase__+'16103.jpg',0,2)
    addDir('Moto(s)poušť','13432',4,__dmdbase__+'13432.jpg',0,2)
    addDir('Největší bitvy II. světové války','16421',4,__dmdbase__+'16421.jpg',0,2)
    addDir('Spartakus: Krev a písek','15767',4,__dmdbase__+'15767.jpg',0,2)
    addDir('Těžká dřina','12317',4,__dmdbase__+'12317.jpg',0,2)
    addDir('Vítejte doma','14881',4,__dmdbase__+'14881.jpg',0,2)
    addDir('menZone','15766',4,__dmdbase__+'15766.jpg',0,2)
    
def INDEX(url,page,kanal):
    if int(page) != 0:
        strquery = '?method=json&action=relevant&per_page=12&channel='+str(kanal)+'&page='+str(page)
    else:
        strquery = '?method=json&action=relevant&per_page=12&channel='+str(kanal)
    doc = read_page('http://play.iprima.cz/videoarchiv_ajax/all/'+str(url)+strquery)
    tid = re.compile('"tid":"(.+?)"').findall(str(doc))
    match = re.compile('"nid":"(.+?)","title":"(.+?)","image":"(.+?)","date":"(.+?)"').findall(str(doc))
    for videoid,name,thumb,datum in match:
            name = replace_words(name, word_dic)
            thumb = replace_words(thumb, word_dic)
            thumb = re.sub('98x55','280x158',thumb)
            addDir(str(name),'http://play.iprima.cz/iprima/'+videoid+'/',10,'http://www.iprima.cz/'+thumb,'','')
            if kanal == 1:
                addDir(str(name),'http://play.iprima.cz/iprima/'+videoid+'/'+tid[0],10,'http://www.iprima.cz/'+thumb,'','')
            elif kanal == 2:
                addDir(str(name),'http://play.iprima.cz/cool/'+videoid+'/'+tid[0],10,'http://www.iprima.cz/'+thumb,'','')
            elif kanal == 3:
                addDir(str(name),'http://play.iprima.cz/love/'+videoid+'/'+tid[0],10,'http://www.iprima.cz/'+thumb,'','')
    strankovani = re.compile('"total":(.+?),"from":.+?,"to":.+?,"page":(.+?),').findall(str(doc))
    for page_total,act_page in strankovani:
        print page_total,act_page
        if int(page_total) > 12:
            act_page = act_page.replace('"','')
            next_page = int(act_page)  + 1
            max_page =  round(int(page_total)/12 )
            if next_page < max_page+1:
                max_page = str(max_page+1)
                #max_page = re.sub('.0','',max_page)
                #print '>> Další strana >>',url,1,next_page
                addDir('>> Další strana ('+str(next_page+1)+' z '+max_page+')',url,4,nexticon,next_page,kanal)
        
def VIDEOLINK(url,name):
    strquery = '?method=json&action=video'
    request = urllib2.Request(url, strquery)
    con = urllib2.urlopen(request)
    data = con.read()
    con.close()
    print url
    stream_video = re.compile('cdnID=([0-9]+)').findall(data)
    if len(stream_video) > 0:
        print 'LQ '+__cdn_url__+name,stream_video[0],icon,''
        addLink('LQ '+name,__cdn_url__+stream_video[0],icon,'')        
    else:
        hq_stream = re.compile("'hq_id':'(.+?)'").findall(data)
        lq_stream = re.compile("'lq_id':'(.+?)'").findall(data)
        geo_zone = re.compile("'zoneGEO':(.+?),").findall(data)        
        thumb = re.compile("'thumbnail':'(.+?)'").findall(data)
        nahled = 'http://embed.livebox.cz/iprima/'+thumb[0]
        print geo_zone[0]
        key = 'http://embed.livebox.cz/iprimaplay/player-embed-v2.js?__tok'+str(gen_random_decimal(1073741824))+'__='+str(gen_random_decimal(1073741824))
        req = urllib2.Request(key)
        req.add_header('User-Agent', _UserAgent_)
        req.add_header('Referer', url)
        response = urllib2.urlopen(req)
        keydata = response.read()
        response.close()
        keydata = re.compile("auth=(.*?)'").findall(keydata)
        if geo_zone[0] == "1":
            hq_url = 'rtmp://bcastiw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth='+keydata[0]+'/mp4:'+hq_stream[0]
            lq_url = 'rtmp://bcastiw.livebox.cz:80/iprima_token_'+geo_zone[0]+'?auth='+keydata[0]+'/mp4:'+lq_stream[0]
        else:
            hq_url = 'rtmp://bcastnw.livebox.cz:80/iprima_token?auth='+keydata[0]+'/mp4:'+hq_stream[0]
            lq_url = 'rtmp://bcastnw.livebox.cz:80/iprima_token?auth='+keydata[0]+'/mp4:'+lq_stream[0]

            #hq_url = 'rtmp://iprima.livebox.cz/play/'+hq_stream[0]
            #lq_url = 'rtmp://iprima.livebox.cz/play/'+lq_stream[0]
            
        print nahled, hq_url, lq_url
        if __settings__.getSetting('kvalita_sel') == "true":
            print 'HQ '+name,hq_url,nahled,name
            addLink('HQ '+name,hq_url,nahled,name)
        if __settings__.getSetting('kvalita_sel') == "false":
            print 'LQ '+name,lq_url,nahled,name
            addLink('LQ '+name,lq_url,nahled,name)

def gen_random_decimal(d):
        return decimal.Decimal('%d' % (random.randint(0,d)))

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

def addDir(name,url,mode,iconimage,page,kanal):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&page="+str(page)+"&kanal="+str(kanal)
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
kanal=None
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
try:
        kanal=int(params["kanal"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Page: "+str(page)
print "Kanal: "+str(kanal)

if mode==None or url==None or len(url)<1:
        print ""
        OBSAH()
       
elif mode==1:
        print ""
        OBSAH_FAMILY(url)
elif mode==2:
        print ""
        OBSAH_LOVE(url)
elif mode==3:
        print ""
        OBSAH_COOL(url)
elif mode==4:
        print ""+str(url)
        print ""+str(kanal)
        print ""+str(page)
        INDEX(url,page,kanal)
        
elif mode==10:
        print ""+url
        VIDEOLINK(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
