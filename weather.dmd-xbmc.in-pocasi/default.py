# -*- coding: utf-8 -*-

# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html

import os, sys, socket, urllib2
from xml.dom import minidom
import xbmc, xbmcgui, xbmcaddon
import re, datetime
import math

#Nacteni informaci o doplnku
__addon__      = xbmcaddon.Addon()
__addonname__  = __addon__.getAddonInfo('name')
__addonid__    = __addon__.getAddonInfo('id')
__cwd__        = __addon__.getAddonInfo('path').decode("utf-8")
__language__   = __addon__.getLocalizedString

#Nastaveni pozadi
#__resource__   = xbmc.translatePath( os.path.join( __cwd__, 'resources', 'pozadi' ).encode("utf-8") ).decode("utf-8")
#xbmc.executebuiltin('Skin.SetString(WeatherFanartDir,'+__resource__+'/)')
#xbmc.executebuiltin('Skin.SetString(CustomBackgroundPath,'+__resource__+'\pozadi2.jpg)')
#xbmc.executebuiltin('Skin.SetBol(UseCustomBackground, True)')

#Obecna nastaveni
_UserAgent_ = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
WEATHER_WINDOW   = xbmcgui.Window(12600)
socket.setdefaulttimeout(10)

#Přiřazení statusu k ikonkám počasí
weatherid = ['bourky', 'dest', 'jasno-noc', 'jasno', 'kroupy', 'mlha', 'obcasny-dest', 'oblacno', 'oblacno-noc', 'polojasno-noc', 'polojasno', 'prehanky-bourky-noc', 'prehanky-bourky', 'prehanky-dest-noc', 'prehanky-dest', 'prehanky-snih-dest-noc', 'prehanky-snih-dest', 'prehanky-snih-noc', 'prehanky-snih', 'skorojasno-bourky-noc', 'skorojasno-bourky', 'skorojasno-noc', 'skorojasno-prehanky-noc', 'skorojasno-prehanky', 'skorojasno', 'snih-dest', 'snih', 'zatazeno']
weathericonid = ['38', '1', '31', '32', '35', '21', '11', '26', '26', '27', '28', '47', '4', '45', '9', '46', '14', '46', '14', '47', '38', '33', '45', '30', '34', '5', '16', '26']

#Vypisování českých dnů
czdays = ['Neděle', 'Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota', 'Neděle', 'Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek', 'Sobota', 'Neděle']
den = datetime.datetime.now()
den = int(den.strftime("%w"))
print 'den: %s' %den


#Nastaveni hodnot o pocasi
def set_property(name, value):
    WEATHER_WINDOW.setProperty(name, value)

    
#Nacte data o pocasi ze serveru
def parse_data():
    #Stahnuti dat
    mestoid = __addon__.getSetting('mestoid')
    req = urllib2.Request('http://www.in-pocasi.cz/iphone/data.php?mesto=%s&stanice=%s&text=ano&aktualita=ano'%(mestoid, mestoid))
    req.add_header('User-Agent', _UserAgent_)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    link=response.read()
    response.close()
    print httpdata
    #0: 17|13|obcasny-dest|obcasny-dest|oblacno|obcasny-dest|zatazeno 1
    
    #Parsovani predovedi na 6 dnu (vcetne dneska)
    for count in range (0, 5):
        match = re.compile('%s: (.+?)\|(.+?)\|(.+?)\n'%count).findall(httpdata)
        for max, min, odpo in match:
            set_property('Day%s.Title'      %count  , czdays[den+count])#DAYS[item.attributes['day'].value]
            set_property('Day%s.HighTemp'   %count  , max)
            set_property('Day%s.LowTemp'    %count  , min)
            set_property('Day%s.OutlookIcon'%count  , xbmc.translatePath(os.path.join(__cwd__, 'resources/lib/icons', '%s.png'%odpo)))   
            set_property('Day%s.FanartCode' %count  , '31')
        match = re.compile('text%s: (.+?\.)'%count).findall(httpdata)
        for vyhled in match:    
            set_property('Day%s.Outlook'%count     , "[COLOR white]%s[/COLOR]"%vyhled.replace("se ","[COLOR white]se [/COLOR]").replace("s ","[COLOR white]s [/COLOR]")) #Mensi hack, aby se neprevadela slova "s" na N a "se" na JV
    
    #Aktualni informace o pocasi
    match = re.compile('now: .+?\|(.+?)\|.+?\|(.+?)\|(.+?)\|(.+?)\|.+?\|.+?\|.+?\|.+?\|.+?\|(.+?)\|.+?\n').findall(httpdata)
    for teplota, rychlost, smer, vlhkost, stav in match:
        set_property('Current.Location'      , __addon__.getSetting('mesto'))
        set_property('Current.Temperature'   , teplota)
        set_property('Current.Wind'          , str(float(rychlost)*3.6))
        set_property('Current.WindDirection' , smer)
        #set_property('Current.WindChill'    , wind[0].attributes['chill'].value)
        set_property('Current.Humidity'      , vlhkost)
        #set_property('Current.Visibility'   , atmosphere[0].attributes['visibility'].value)
        #set_property('Current.Pressure'     , atmosphere[0].attributes['pressure'].value)
        set_property('Current.FeelsLike'     , feelslike(int(teplota), int(round(float(rychlost)*3.6) + 0.5)))
        set_property('Current.DewPoint'      , dewpoint(int(teplota), int(vlhkost)))
        set_property('Current.UVIndex'       , '-')
        index = 0;
        print 'Stav: '+stav
        set_property('Current.OutlookIcon', xbmc.translatePath(os.path.join(__cwd__, 'resources/lib/icons', '%s.png'%stav)))
        #for icon in weatherid:
        #    if icon == stav:
        #        set_property('Current.OutlookIcon', '%s.png'%weathericonid[index])   
        #        print 'ID obrazku: '+weathericonid[index]
        #        print 'Stav: '+stav
        #    index = index+1
        set_property('Current.FanartCode'    , '20')
        #set_property('Today.Sunrise'        , astronomy[0].attributes['sunrise'].value)
        #set_property('Today.Sunset'         , astronomy[0].attributes['sunset'].value)
    
    #Ziskani aktuality
    match = re.compile('aktual: .+?\|(.*)').findall(httpdata)
    for aktualita in match:
        #aktualita = "O víkendu se s přidají přeháňky nebo i bouřky"
        set_property('Current.Condition'     , "[COLOR white]%s[/COLOR]"%aktualita.replace("se ","[COLOR white]se [/COLOR]").replace("s ","[COLOR white]s [/COLOR]"))
    
    
def clear(): #Vynulovani hodnot pred stazenim novych
    set_property('Current.Condition'     , 'N/A')
    set_property('Current.Temperature'   , '0')
    set_property('Current.Wind'          , '0')
    set_property('Current.WindDirection' , 'N/A')
    set_property('Current.Humidity'      , '0')
    set_property('Current.FeelsLike'     , '0')
    set_property('Current.UVIndex'       , '0')
    set_property('Current.DewPoint'      , '0')
    set_property('Current.OutlookIcon'   , 'na.png')
    set_property('Current.FanartCode'    , 'na')
    for count in range (0, 5):
        set_property('Day%i.Title'       % count, 'N/A')
        set_property('Day%i.HighTemp'    % count, '0')
        set_property('Day%i.LowTemp'     % count, '0')
        set_property('Day%i.Outlook'     % count, 'N/A')
        set_property('Day%i.OutlookIcon' % count, 'na.png')
        set_property('Day%i.FanartCode'  % count, 'na')


def feelslike( T=10, V=25 ): #Pomocna funkce pro vypocet pocitove teploty
    """ The formula to calculate the equivalent temperature related to the wind chill is:
        T(REF) = 13.12 + 0.6215 * T - 11.37 * V**0.16 + 0.3965 * T * V**0.16
        Or:
        T(REF): is the equivalent temperature in degrees Celsius
        V: is the wind speed in km/h measured at 10m height
        T: is the temperature of the air in degrees Celsius
        source: http://zpag.tripod.com/Meteo/eolien.htm
        
        getFeelsLike( tCelsius, windspeed )
    """
    FeelsLike = T
    #Wind speeds of 4 mph or less, the wind chill temperature is the same as the actual air temperature.
    if round( ( V + .0 ) / 1.609344 ) > 4:
        FeelsLike = ( 13.12 + ( 0.6215 * T ) - ( 11.37 * V**0.16 ) + ( 0.3965 * T * V**0.16 ) )
    return str( round( FeelsLike ) )


def dewpoint( Tc=0, RH=93, minRH=( 0, 0.075 )[ 0 ] ): #Pomocna funkce pro vypocet rosneho bodu
    """ Dewpoint from relative humidity and temperature
        If you know the relative humidity and the air temperature,
        and want to calculate the dewpoint, the formulas are as follows.
        
        getDewPoint( tCelsius, humidity )
    """
    #First, if your air temperature is in degrees Fahrenheit, then you must convert it to degrees Celsius by using the Fahrenheit to Celsius formula.
    # Tc = 5.0 / 9.0 * ( Tf - 32.0 )
    #The next step is to obtain the saturation vapor pressure(Es) using this formula as before when air temperature is known.
    Es = 6.11 * 10.0**( 7.5 * Tc / ( 237.7 + Tc ) )
    #The next step is to use the saturation vapor pressure and the relative humidity to compute the actual vapor pressure(E) of the air. This can be done with the following formula.
    #RH=relative humidity of air expressed as a percent. or except minimum(.075) humidity to abort error with math.log.
    RH = RH or minRH #0.075
    E = ( RH * Es ) / 100
    #Note: math.log( ) means to take the natural log of the variable in the parentheses
    #Now you are ready to use the following formula to obtain the dewpoint temperature.
    try:
        DewPoint = ( -430.22 + 237.7 * math.log( E ) ) / ( -math.log( E ) + 19.08 )
    except ValueError:
        #math domain error, because RH = 0%
        #return "N/A"
        DewPoint = 0 #minRH
    #Note: Due to the rounding of decimal places, your answer may be slightly different from the above answer, but it should be within two degrees.
    return str( int( DewPoint ) )
    
def settings():
    #Nacti soubor se seznamem mest
    mestasoubor = open(xbmc.translatePath(os.path.join(__cwd__, 'resources', 'mesta-list.xml')), 'r')
    mestadata   = mestasoubor.read()
    mestadata   = mestadata.replace("\r","")
    mestadata   = mestadata.replace("\n","")
    mestadata   = mestadata.replace("\t","")
    
    #Vyparsuj a zobraz kraje
    krajelist   = re.compile('<region id=".+?" name="(.+?)">').findall(mestadata)
    dialog      = xbmcgui.Dialog()
    kraj        = dialog.select('Vyberte kraj', krajelist)
    print "Vybraný kraj %s"     %krajelist[kraj]
    
    #Vyparsuj a zobraz mesta
    mestalist1  = re.compile('<region id=".+?" name="%s">(.+?)</region>'%krajelist[kraj]).findall(mestadata)
    print "Mesta %s"            %mestalist1[0]
    mestalist2  = re.compile('<mesto id=".+?" name="(.+?)"').findall(mestalist1[0])
    mestalistid = re.compile('<mesto id="(.+?)" name=".+?"').findall(mestalist1[0])
    print "Mesta seznam: %s"    %mestalist2
    mesto       = dialog.select('Vyberte město', mestalist2)
    print "Vybráno: %s"         %mestalist2[mesto]
    print "Vybráno ID: %s"      %mestalistid[mesto]
    
    #Uloz nastaveni
    __addon__.setSetting('mesto', mestalist2[mesto])
    __addon__.setSetting('mestoid', mestalistid[mesto])

    
#HLAVNI PROGRAM

#Zobraz nastaveni
if sys.argv[1].startswith('mesto'): 
    settings()
elif __addon__.getSetting('mestoid') == '': 
    settings()

#Vycisti data
clear()   
      
#Dopln aktualni data
parse_data()    

#Vseobecne informace
set_property('Location1',           __addon__.getSetting('mesto'))
set_property('Locations',           str(1)) #pocet lokaci celkem (mame pouze jedno) Je treba, jinak nezobrazi misto
set_property('WeatherProvider',     __addonname__)
set_property('WeatherProviderLogo', xbmc.translatePath(os.path.join(__cwd__, 'resources', 'banner.png')))

