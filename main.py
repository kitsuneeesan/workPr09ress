import os
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'workPr09ress'

def change_label(ind_app, percent=0):
    def progress(percent=0, widht=30):
        left = widht * percent // 100
        right = widht - left
        return ',' * left + '.' * right + f'{percent:.0f}%'
    
    def get_uptime():
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        return int(uptime_seconds)
        
    if percent == 100:percent = 0
    else:percent = int(get_uptime() / 32400 * 100)

    ind_app.set_label(progress(percent), '')
    GLib.timeout_add(1000, lambda: change_label(ind_app, percent))

def quit(source):
    Gtk.main_quit()

ind_app = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('train-svgrepo-com.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
ind_app.set_status(appindicator.IndicatorStatus.ACTIVE)

menu = Gtk.Menu()
menu_items = Gtk.MenuItem("Exit")
menu.append(menu_items)
menu_items.connect("activate", quit)
menu_items.show_all()
ind_app.set_menu(menu)

change_label(ind_app)
Gtk.main()