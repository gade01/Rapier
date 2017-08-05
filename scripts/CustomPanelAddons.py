# *  Thanks to:
# *
# *  Nuka for the original RecentlyAdded.py
# *
# *  ppic, Hitcher & ronie for the RandomItems.py

import xbmc, xbmcgui, os, sys
try:
    from elementtree import ElementTree as xmltree
except:
    import ElementTree as xmltree

class Main:
    # grab the home window
    WINDOW = xbmcgui.Window( 10000 )

    def __init__( self ):
        self._parse_argv()
        self._clear_properties()
        self._fetch_addon_info()
		
    def _parse_argv( self ):
        self.LIMIT = int( "30" )

    def _clear_properties( self ):
        self.WINDOW.clearProperty( "CustomPanelAddon.Count" )
        for count in range( self.LIMIT ):
            # clear Property
            self.WINDOW.clearProperty( "CustomPanelAddon.%d.Name" % ( count + 1 ) )
            self.WINDOW.clearProperty( "CustomPanelAddon.%d.Path" % ( count + 1 ) )			
            self.WINDOW.clearProperty( "CustomPanelAddon.%d.Fanart" % ( count + 1 ) )			
            self.WINDOW.clearProperty( "CustomPanelAddon.%d.Thumb" % ( count + 1 ) )
            self.WINDOW.clearProperty( "CustomPanelAddon.%d.Type" % ( count + 1 ) )

    def _fetch_addon_info( self ):
        # initialize our list
        addonlist = []
        # list the contents of the addons folder
        addonpath = xbmc.translatePath( 'special://home/addons/' )
        addons = os.listdir(addonpath)
        # find directories in the addons folder
        for item in addons:
            if os.path.isdir(os.path.join(addonpath, item)):
                # find addon.xml in the addon folder
                addonfile = os.path.join(addonpath, item, 'addon.xml')
                if os.path.exists(addonfile):
                    # find addon properties
                    addonfilecontents = xmltree.parse(addonfile).getroot()
                    for element in addonfilecontents.getiterator():
                       if element.tag == "addon":
                           addonid = element.attrib.get('id')
                           addonname = element.attrib.get('name')
                       elif element.tag == "provides":
                           addonprovides = element.text
                    # add addons to list
                    try:
                        if (addonprovides == 'video') or (addonprovides == 'audio') \
                        or (addonprovides == 'image') or (addonprovides == 'executable'):
                            addonthumb = os.path.join(addonpath, item, 'icon.png')
                            addonfanart = os.path.join(addonpath, item, 'fanart.jpg')
                            addonlist.append( (addonname, addonid, addonfanart, addonthumb, addonprovides) )
                            # clean addon provides
                            addonprovides = []
                    except:
                        pass
        # get total value
        total = str( len( addonlist ) )
        # count thru our addons
        count = 0
        while count < self.LIMIT:
            count += 1
            # check if we don't run out of items before LIMIT is reached
            if len(addonlist) == 0:
                return
            # select first item
            addonid = addonlist[0]
            # remove the item from our list
            addonlist.remove(addonid)
            # set properties
            self.WINDOW.setProperty( "CustomPanelAddon.%d.Name"    % ( count ), addonid[0] )
            self.WINDOW.setProperty( "CustomPanelAddon.%d.Path"    % ( count ), addonid[1] )
            self.WINDOW.setProperty( "CustomPanelAddon.%d.Fanart"  % ( count ), addonid[2] )
            self.WINDOW.setProperty( "CustomPanelAddon.%d.Thumb"   % ( count ), addonid[3] )
            self.WINDOW.setProperty( "CustomPanelAddon.%d.Type"    % ( count ), addonid[4] )
            self.WINDOW.setProperty( "CustomPanelAddon.Count"      , total )

if ( __name__ == "__main__" ):
    Main()
