import os
import sys
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'workPr09ress'
help = """[--help] 
    -h : to set with hours
    -m : to set with minutes
    -s : to set with seconds
    *note : just only use 1 arg!"""

avail_args = {'-h': 0, '-m': 0, '-s': 0, '--help': help}
use_args = sys.argv[1:]

try:
    if '--help' in use_args:
        print(avail_args['--help'])
        exit()
    elif use_args[0] not in list(avail_args.keys()):
        print(f'unknow option : {use_args[0]}\n', help)
        exit()

    avail_args[use_args[0]] = use_args[1]
except Exception as e:
    pass


def get_set_time(args):
    args.pop("--help", None)
    for k, v in args.items():
        if v:
            if k == '-h':
                return int(v) * 3600
            elif k == '-m':
                return int(v) * 60
            else:
                return int(v)


set_time = get_set_time(avail_args) or 32400


def change_label(ind_app, percent=0, set_time=set_time, **kwargs):
    over_time = kwargs.get('over_time', False)
    over_time_label = 'YOU ARE THE CHAMPIONS!'
    over_time_label_index = kwargs.get('over_time_label_index', False) or 0

    def progress(percent=0, widht=30):
        left = widht * percent // 100
        right = widht - left
        return ',' * left + '.' * right + f'{percent:.0f}%'

    def get_uptime():
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        return int(uptime_seconds)

    percent = int(get_uptime() / set_time * 100)
    label = progress(percent) if not over_time else over_time_label[0:over_time_label_index]
    ind_app.set_label(label, '')
    
    over_time = percent > 100
    over_time_label_index = over_time_label_index + 1 if over_time_label_index <= len(over_time_label) else 0
    
    GLib.timeout_add(1000, lambda: change_label(ind_app, percent, set_time, over_time=over_time, over_time_label_index=over_time_label_index))


def quit(source):
    Gtk.main_quit()


ind_app = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(
    '/home/nanda/Documents/workPr09ress/train-svgrepo-com.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
ind_app.set_status(appindicator.IndicatorStatus.ACTIVE)

menu = Gtk.Menu()
menu_items = Gtk.MenuItem("Exit")
menu.append(menu_items)
menu_items.connect("activate", quit)
menu_items.show_all()
ind_app.set_menu(menu)

change_label(ind_app, 0, set_time)
Gtk.main()
