# -*- coding: utf-8 -*-
import urllib2,urllib,re,os
from parseutils import *
import xbmcplugin,xbmcgui,xbmcaddon
import megavideo,videobb,novamov,vk,videoweed,videozer

__baseurl__ = 'http://www.piratskefilmy.cz'
#_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
_UserAgent_ =  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
addon = xbmcaddon.Addon('plugin.video.dmd-czech.piratskefilmycz')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.dmd-czech.piratskefilmycz')
home = __settings__.getAddonInfo('path')
REV = os.path.join( profile, 'list_revision')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
nexticon = xbmc.translatePath( os.path.join( home, 'nextpage.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )


#==========================================================================
def OBSAH():
    addDir('Hledat ...',__baseurl__,7,icon)
    addDir('Podle kategorie',__baseurl__,1,icon)
    addDir('Podle hercu',__baseurl__,2,icon)
    addDir('Podle roku',__baseurl__,3,icon)
    addDir('Podle serveru',__baseurl__,4,icon)
    addDir('Filmy Online',__baseurl__+'/',5,icon)
#==========================================================================


#==========================================================================
def KATEGORIE():
	addDir('Akční',__baseurl__+'/kategorie/akcni/',5,icon)
	addDir('Animovaný',__baseurl__+'/kategorie/animovany/',5,icon)
	addDir('Dobrodružný',__baseurl__+'/kategorie/dobrodruzny/',5,icon)
	addDir('Dokumentární',__baseurl__+'/kategorie/dokumentarni/',5,icon)
	addDir('Drama',__baseurl__+'/kategorie/drama/',5,icon)
	addDir('Erotický',__baseurl__+'/kategorie/eroticky/',5,icon)
	addDir('Fantasy',__baseurl__+'/kategorie/fantasy/',5,icon)
	addDir('Historický',__baseurl__+'/kategorie/historicky/',5,icon)
	addDir('Horory',__baseurl__+'/kategorie/horory/',5,icon)
	addDir('Hudební',__baseurl__+'/kategorie/hudebni/',5,icon)
	addDir('IMAX',__baseurl__+'/kategorie/imax/',5,icon)
	addDir('Katastrofický',__baseurl__+'/kategorie/katastroficky/',5,icon)
	addDir('Komedie',__baseurl__+'/kategorie/komedie/',5,icon)
	addDir('Krátkometrážní',__baseurl__+'/kategorie/kratkometrazni/',5,icon)
	addDir('Krimi',__baseurl__+'/kategorie/krimi/',5,icon)
	addDir('Loutkový',__baseurl__+'/kategorie/loutkovy/',5,icon)
	addDir('Muzikál',__baseurl__+'/kategorie/muzikal/',5,icon)
	addDir('Mysteriózní',__baseurl__+'/kategorie/mysteriozni/',5,icon)
	addDir('Nezařazené',__baseurl__+'/kategorie/nezarazene/',5,icon)
	addDir('Podobenství',__baseurl__+'/kategorie/podobenstvi/',5,icon)
	addDir('Poetický',__baseurl__+'/kategorie/poeticky/',5,icon)
	addDir('Pohádky',__baseurl__+'/kategorie/pohadky/',5,icon)
	addDir('Povídkový',__baseurl__+'/kategorie/povidkovy/',5,icon)
	addDir('Psychologický',__baseurl__+'/kategorie/psychologicky/',5,icon)
	addDir('Rodinné',__baseurl__+'/kategorie/rodinne/',5,icon)
	addDir('Romantické',__baseurl__+'/kategorie/romanticke/',5,icon)
	addDir('Sci-fi',__baseurl__+'/kategorie/sci-fi/',5,icon)
	addDir('Sportovní',__baseurl__+'/kategorie/sportovni/',5,icon)
	addDir('Talk-show',__baseurl__+'/kategorie/talk-show/',5,icon)
	addDir('Thrillery',__baseurl__+'/kategorie/thrillery/',5,icon)
	addDir('Válečný',__baseurl__+'/kategorie/valecny/',5,icon)
	addDir('Western',__baseurl__+'/kategorie/western/',5,icon)
	addDir('Životopisný',__baseurl__+'/kategorie/zivotopisny/',5,icon)
#==========================================================================

#==========================================================================
def HERCI():
	addDir('Brian Cox',__baseurl__+'/herec/brian-cox/',5,icon) 
	addDir('Bruce Willis',__baseurl__+'/herec/bruce-willis/',5,icon) 
	addDir('Christopher McDonald',__baseurl__+'/herec/christopher-mcdonald/',5,icon) 
	addDir('Christopher Walken',__baseurl__+'/herec/christopher-walken/',5,icon) 
	addDir('Danny DeVito',__baseurl__+'/herec/danny-devito/',5,icon) 
	addDir('Danny Glover',__baseurl__+'/herec/danny-glover/',5,icon) 
	addDir('Danny Trejo',__baseurl__+'/herec/danny-trejo/',5,icon) 
	addDir('Donald Sutherland',__baseurl__+'/herec/donald-sutherland/',5,icon) 
	addDir('Dustin Hoffman',__baseurl__+'/herec/dustin-hoffman/',5,icon) 
	addDir('Eugene Levy',__baseurl__+'/herec/eugene-levy/',5,icon) 
	addDir('Frank Welker',__baseurl__+'/herec/frank-welker/',5,icon) 
	addDir('František Filipovský',__baseurl__+'/herec/frantisek-filipovsky/',5,icon) 
	addDir('Jackie Chan',__baseurl__+'/herec/jackie-chan/',5,icon) 
	addDir('Jan Kuželka',__baseurl__+'/herec/jan-kuzelka/',5,icon) 
	addDir('Jaroslav Marvan',__baseurl__+'/herec/jaroslav-marvan/',5,icon) 
	addDir('Jiří Lábus',__baseurl__+'/herec/jiri-labus/',5,icon) 
	addDir('Jiří Lír',__baseurl__+'/herec/jiri-lir/',5,icon) 
	addDir('Jim Cummings',__baseurl__+'/herec/jim-cummings/',5,icon) 
	addDir('John Di Maggio',__baseurl__+'/herec/john-di-maggio/',5,icon) 
	addDir('John Malkovich',__baseurl__+'/herec/john-malkovich/',5,icon) 
	addDir('Johnny Depp',__baseurl__+'/herec/johnny-depp/',5,icon) 
	addDir('Josef Somr',__baseurl__+'/herec/josef-somr/',5,icon) 
	addDir('Justin Long',__baseurl__+'/herec/justin-long/',5,icon) 
	addDir('Karel Augusta',__baseurl__+'/herec/karel-augusta/',5,icon) 
	addDir('Keith David',__baseurl__+'/herec/keith-david/',5,icon) 
	addDir('Liam Neeson',__baseurl__+'/herec/liam-neeson/',5,icon) 
	addDir('Lin Shaye',__baseurl__+'/herec/lin-shaye/',5,icon) 
	addDir('Luis Guzmán',__baseurl__+'/herec/luis-guzman/',5,icon) 
	addDir('Matt Damon',__baseurl__+'/herec/matt-damon/',5,icon) 
	addDir('Michael Caine',__baseurl__+'/herec/michael-caine/',5,icon) 
	addDir('Michael Clarke Duncan',__baseurl__+'/herec/michael-clarke-duncan/',5,icon) 
	addDir('Michael Madsen',__baseurl__+'/herec/michael-madsen/',5,icon) 
	addDir('Miroslav Táborský',__baseurl__+'/herec/miroslav-taborsky/',5,icon) 
	addDir('Morgan Freeman',__baseurl__+'/herec/morgan-freeman/',5,icon) 
	addDir('Nicolas Cage',__baseurl__+'/herec/nicolas-cage/',5,icon) 
	addDir('Peter Stormare',__baseurl__+'/herec/peter-stormare/',5,icon) 
	addDir('R. Lee Ermey',__baseurl__+'/herec/r-lee-ermey/',5,icon) 
	addDir('Robert De Niro',__baseurl__+'/herec/robert-de-niro/',5,icon) 
	addDir('Samuel L. Jackson',__baseurl__+'/herec/samuel-l-jackson/',5,icon) 
	addDir('Sigourney Weaver',__baseurl__+'/herec/sigourney-weaver/',5,icon) 
	addDir('Stella Zázvorková',__baseurl__+'/herec/stella-zazvorkova/',5,icon) 
	addDir('Steve Buscemi',__baseurl__+'/herec/steve-buscemi/',5,icon) 
	addDir('Steven Seagal',__baseurl__+'/herec/steven-seagal/',5,icon) 
	addDir('Val Kilmer',__baseurl__+'/herec/val-kilmer/',5,icon) 
	addDir('Willem Dafoe',__baseurl__+'/herec/willem-dafoe/',5,icon) 
#==========================================================================


#==========================================================================
def ROKY():
	addDir('2011',__baseurl__+'/search/(2011)/',5,icon)
        addDir('2010',__baseurl__+'/search/(2010)/',5,icon)
        addDir('2009',__baseurl__+'/search/(2009)/',5,icon)
        addDir('2008',__baseurl__+'/search/(2008)/',5,icon)
        addDir('2007',__baseurl__+'/search/(2007)/',5,icon)
        addDir('2006',__baseurl__+'/search/(2006)/',5,icon)
        addDir('2005',__baseurl__+'/search/(2005)/',5,icon)
        addDir('2004',__baseurl__+'/search/(2004)/',5,icon)
        addDir('2003',__baseurl__+'/search/(2003)/',5,icon)
        addDir('2002',__baseurl__+'/search/(2002)/',5,icon)
        addDir('2001',__baseurl__+'/search/(2001)/',5,icon)
        addDir('2000',__baseurl__+'/search/(2000)/',5,icon)
        addDir('1999',__baseurl__+'/search/(1999)/',5,icon)
        addDir('1998',__baseurl__+'/search/(1998)/',5,icon)
        addDir('1997',__baseurl__+'/search/(1997)/',5,icon)
        addDir('1996',__baseurl__+'/search/(1996)/',5,icon)
        addDir('1995',__baseurl__+'/search/(1995)/',5,icon)
        addDir('1994',__baseurl__+'/search/(1994)/',5,icon)
        addDir('1993',__baseurl__+'/search/(1993)/',5,icon)
        addDir('1992',__baseurl__+'/search/(1992)/',5,icon)
        addDir('1991',__baseurl__+'/search/(1991)/',5,icon)
        addDir('1990',__baseurl__+'/search/(1990)/',5,icon)
        addDir('1989',__baseurl__+'/search/(1989)/',5,icon)
        addDir('1988',__baseurl__+'/search/(1988)/',5,icon)
        addDir('1987',__baseurl__+'/search/(1987)/',5,icon)
        addDir('1986',__baseurl__+'/search/(1986)/',5,icon)
        addDir('1985',__baseurl__+'/search/(1985)/',5,icon)
        addDir('1984',__baseurl__+'/search/(1984)/',5,icon)
        addDir('1983',__baseurl__+'/search/(1983)/',5,icon)
        addDir('1982',__baseurl__+'/search/(1982)/',5,icon)
        addDir('1981',__baseurl__+'/search/(1981)/',5,icon)
        addDir('1980',__baseurl__+'/search/(1980)/',5,icon)
#==========================================================================

#==========================================================================
def SERVERY():
	addDir('Megavideo.com',__baseurl__+'/search/megavideo.com/',5,icon)
        addDir('Novamov.com',__baseurl__+'/search/novamov.com/',5,icon)
        addDir('Putlocker.com',__baseurl__+'/search/putlocker.com/',5,icon)
        addDir('Videobb.com',__baseurl__+'/search/videobb.com/',5,icon)
        addDir('Videoweed.com',__baseurl__+'/search/videoweed.com/',5,icon)
#==========================================================================

#==========================================================================
searchurl = __baseurl__+'/?s='
def SEARCH():
	keyb = xbmc.Keyboard('', 'Search Filmy CSP')
        keyb.doModal()
        if (keyb.isConfirmed()):
        	search = keyb.getText()
	        encode=urllib.quote(search)
		INDEX(searchurl+encode)
#==========================================================================


#==========================================================================
def INDEX(url):
    doc = read_page(url)  
    items = doc.findAll('div','post')
    for item in items:
	    item2 = item.find('a')
	    if item2 is None:
		    continue
            name = item2.getText(" ").encode('utf-8')
            link = item2['href']
	    item = item.find('img')
            icon = item['src']
            if icon.find('http://') == -1:
            	icon= __baseurl__+item['src'][1:]
            try:
                item2 = item.findParent()
                popis = item2.getText(" ").encode('utf-8')
            except:
                popis=''

            addDir(name,link,6,icon,popis)

    try:
	pager = doc.find('li','page_info')
    	act_page = pager.getText(" ").encode('utf-8')
	act_page = act_page.split(' ')
	max_page = act_page[3]    
	act_page = act_page[1]
	pager = doc.find(id='wp_page_numbers')
    	items = pager.findAll('a')
	for item in items:
		if item.getText(" ").encode('utf-8') != '>':
			continue
		else:
			next_page_a = item['href']
    	next_page = int(act_page) + 1
    	if (int(next_page) > int(max_page)):
 		next_page=max_page
	next_label = 'Přejít na stranu '+str(next_page)+' z '+max_page
    	addDir(next_label,next_page_a,5,nexticon)
    except:
        print 'stop'
#============================================================================================


#============================================================================================
def KINOTIP_URL(url):
	req = urllib2.Request(url)
    	req.add_header('User-Agent',_UserAgent_)
    	response = urllib2.urlopen(req)
    	data=response.read()
 	match=re.compile('<iframe.* src=\'(.+?)\'.*>').findall(data)
    	url=match[0].replace('&#038;','&')
	return url
#============================================================================================

#============================================================================================
def VIDEOBB_LINK(url,name):
	try:
		videourl=videobb.getURL(url)
    		addLink(name+" - videobb.com",videourl,'','')
	except:
		print "VIDEOBB URL: "+url
#============================================================================================

#==========================================================================
def NOVAMOV_LINK(url,name):
	try:
		url=KINOTIP_URL(url)
		#	
		videourl=novamov.getURL(url)
    		addLink(name+" - novamov.com",videourl,'','')
	except:
       		print "NOVAMOV.COM URL: "+url
#==========================================================================

#==========================================================================
def VKCOM_LINK(url,name):
	try:
		videourl=vk.getURL(url)
    		addLink(name+" - vk.com",videourl,'','')
	except:
       		print "VK.COM URL: "+url
#==========================================================================


#==========================================================================
def MEGAVIDEO_LINK(url,name):
 	try:
 		url=megavideo.getcode(url)
 		videourl=megavideo.getURL(url)
 		#addLink(name+" - megavideo.com",videourl,'','')
 		for video_url in videourl:
                      addLink(name+" - "+video_url[0] ,video_url[1],'','')
 	except:
        	print "MEGAVIDEO.COM URL: "+url
#==========================================================================



#==========================================================================
def VIDEOWEED_LINK(url,name):
	try:
		url=KINOTIP_URL(url)
		#
		videourl=videoweed.getURL(url)
    		addLink(name+" - videoweed.com",videourl,'','')
	except:
       		print "VIDEOWEED.COM URL: "+url
#==========================================================================



#==========================================================================
def VIDEOZER_LINK(url,name):
        try:
                #url=KINOTIP_URL(url)
                #
                videourl=videozer.getURL(url)
                addLink(name+" - videozer.com",videourl,'','')
        except:
                print "VIDEOZER.COM URL: "+url
#==========================================================================





#==========================================================================
def VIDEOLINK(url,name):
    print "URL: "+url
    req = urllib2.Request(url)
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    link = response.read()
    match=re.compile('.*(Zdroj.+?)<.*\s.*(<a href|embed src)=\"(.+?)\".*>').findall(link)
    if len(match) <= 0:
	    #/param><embed src="http://www.megavideo.com/v/" type="application/x-shockwave-flash" allowfullscreen="true" width="480" height="400"></embed>
	    match=re.compile('.*(/param>)<.*\s.*(<a href|embed src)=\"(.+?)\".*>').findall(link)
    print match
    for item in match:
	#name = item[0]
    	item = item[2].replace('&amp;','&')
	if item.find('videobb.com') != -1:
		VIDEOBB_LINK(item,name)
	elif item.find('novamov.php?id=') != -1:
		NOVAMOV_LINK(item,name)
	elif item.find('megavideo.com') != -1:
		MEGAVIDEO_LINK(item,name)
	elif item.find('videoweed.php?id=') != -1:
		VIDEOWEED_LINK(item,name)
        elif item.find('videozer.com') != -1:
                VIDEOZER_LINK(item,name)
	elif item.find('vk.com') != -1 or item.find('vkontakte.ru') != -1:
		VKCOM_LINK(item,name)
	else:
		print "VIDEOLINK URL: "+item

	

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

def addDir(name,url,mode,iconimage,popis=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        #liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": popis} )
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
        KATEGORIE()

elif mode==2:
        print ""+url
        HERCI()
        
elif mode==3:
        print ""+url
        ROKY()
        
elif mode==4:
        print ""+url
        SERVERY()
        
elif mode==5:
        print ""+url
        INDEX(url)
        
elif mode==6:
        print ""+url
        VIDEOLINK(url,name)

elif mode==7:
        print ""+url
        SEARCH()

xbmcplugin.endOfDirectory(int(sys.argv[1]))


