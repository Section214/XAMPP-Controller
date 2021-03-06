#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# XAMPP Controller
# A simple controller for XAMPP on Unity
#
# Copyright (c) 2014 Daniel J Griffiths <dgriffiths@section214.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gtk
import gobject
import appindicator
import os
import pynotify
import sys
import shlex
import re
import commands
import webbrowser

_VERSION = "1.0.5"

_ABOUT_TXT = """A simple Ubuntu app indicator for XAMPP.

<small><a href="http://section214.com">Website</a>   <a href="http://support.section214.com">Support</a>   <a href="https://twitter.com/intent/user?screen_name=ghost1227">Follow Me On Twitter</a></small>

<small>Copyright 2014 Daniel J Griffiths &lt;<a href="mailto:dgriffiths@section214.com">dgriffiths@section214.com</a>&gt;</small>
<small>XAMPP is an open source web server stack developed by <a href="https://www.apachefriends.org/">Apache Friends</a>.</small>"""

def menuitem_response(w, item):
    if item == '_about':
        show_help_dlg(_ABOUT_TXT)
    elif item == '_quit':
        sys.exit(0);
    elif item == '_refresh':
        newmenu = build_menu()
        ind.set_menu(newmenu)
    elif item == 'folder':
        pass
    else:
        if 'http' in item:
            webbrowser.open(item,new=2)
        else:
            os.system(item)
            if 'gksudo' in item:
                newmenu = build_menu()
                ind.set_menu(newmenu)

def show_help_dlg(msg):
    md = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK)

    # Override dialog icon
    logo = gtk.Image()
    logo.set_from_file(sys.path[0] + '/about-icon.png')
    logo.show()
    md.set_image(logo)

    try:
        md.set_markup("<b>XAMPP Controller - v%s</b>" % _VERSION)
        md.format_secondary_markup(msg)
        md.run()
    finally:
        md.destroy()

def add_separator(menu):
    separator = gtk.SeparatorMenuItem()
    separator.show()
    menu.append(separator)

def add_menu_item(menu, caption, item=None):
    menu_item = gtk.MenuItem(caption)
    
    if item:
        menu_item.connect("activate", menuitem_response, item)
    else:
        menu_item.set_sensitive(False)    
    
    menu_item.show()
    menu.append(menu_item)

    return menu_item

def build_menu():
    menu = gtk.Menu()
    apacheMenu = gtk.Menu()
    mysqlMenu = gtk.Menu()
    ftpMenu = gtk.Menu()

    running = commands.getoutput('ps -A')

    # Master control
    if not 'lampp/bin' in running:
        add_menu_item(menu, 'Start XAMPP', 'gksudo --description "XAMPP" /opt/lampp/lampp start')
    else:
        add_menu_item(menu, 'Restart XAMPP', 'gksudo --description "XAMPP" /opt/lampp/lampp restart')
        add_menu_item(menu, 'Stop XAMPP', 'gksudo --description "XAMPP" /opt/lampp/lampp stop')

    add_separator(menu)

    add_menu_item(menu, 'Control Services', None)

    # Apache menu
    menu_item = add_menu_item(menu, 'Apache', 'folder')
    menu_item.set_submenu(apacheMenu)

    if not 'lampp/bin' in running:
        add_menu_item(apacheMenu, 'Start', 'gksudo --description "XAMPP" /opt/lampp/lampp startapache')
    else:
        add_menu_item(apacheMenu, 'Stop', 'gksudo --description "XAMPP" /opt/lampp/lampp stopapache')
        add_menu_item(apacheMenu, 'Reload Config', 'gksudo --description "XAMPP" /opt/lampp/lampp reloadapache')
        
    # MySQL menu
    menu_item = add_menu_item(menu, 'MySQL', 'folder')
    menu_item.set_submenu(mysqlMenu)

    if not 'mysqld' in running:
        add_menu_item(mysqlMenu, 'Start', 'gksudo --description "XAMPP" /opt/lampp/lampp startmysql')
    else:
        add_menu_item(mysqlMenu, 'Stop', 'gksudo --description "XAMPP" /opt/lampp/lampp stopmysql')
        add_menu_item(mysqlMenu, 'Reload Config', 'gksudo --description "XAMPP" /opt/lampp/lampp reloadmysql')

    # FTP menu
    menu_item = add_menu_item(menu, 'ProFTPD', 'folder')
    menu_item.set_submenu(ftpMenu)

    if not 'proftpd' in running:
        add_menu_item(ftpMenu, 'Start', 'gksudo --description "XAMPP" /opt/lampp/lampp startftp')
    else:
        add_menu_item(ftpMenu, 'Stop', 'gksudo --description "XAMPP" /opt/lampp/lampp stopftp')
        add_menu_item(ftpMenu, 'Reload Config', 'gksudo --description "XAMPP" /opt/lampp/lampp reloadftp')

    add_separator(menu)

    # Web views
    add_menu_item(menu, 'Web Views', None)
    
    root_url = 'http://localhost/'

    add_menu_item(menu, 'XAMPP Homepage', root_url + 'xampp/index.php')
    add_menu_item(menu, 'phpMyAdmin', root_url + 'phpmyadmin')
    add_menu_item(menu, 'Webalizer', root_url + 'xampp/webalizer.php')

    add_separator(menu)

    # Sites
    add_menu_item(menu, 'Sites', None)

    htdocs = '/opt/lampp/htdocs/' # KISS
    add_menu_item(menu, 'Browse htdocs', 'nautilus ' + htdocs)

    # Find all the sites!
    sites = os.listdir(htdocs)

    for site in sites:
        if os.path.isdir(htdocs + site) and site != 'webalizer' and site != 'img' and site != 'xampp':
            menu_item = add_menu_item(menu, site, 'folder')
            submenu = gtk.Menu()
            menu_item.set_submenu(submenu)

            add_menu_item(submenu, 'Browse Webroot', 'nautilus "' + htdocs + site + '"')
            add_menu_item(submenu, 'View Site', root_url + site)

    add_separator(menu)

    add_menu_item(menu, 'Refresh Menu', '_refresh')

    add_separator(menu)

    add_menu_item(menu, 'About', '_about')
    add_menu_item(menu, 'Quit', '_quit')

    return menu

if __name__ == "__main__":
    ind = appindicator.Indicator(
        "xampp-controller",
        "xampp-controller",
        appindicator.CATEGORY_APPLICATION_STATUS,
        sys.path[0]
    )

    ind.set_status(appindicator.STATUS_ACTIVE)

    appmenu = build_menu()
    ind.set_menu(appmenu)
    gtk.main()
