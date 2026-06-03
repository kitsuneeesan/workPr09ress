import sys
import gi
import cairo
import tempfile

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'workpr09ress'
ICON_TMP = tempfile.mktemp(suffix='.png')
help_text = """[--help]
    -h : set work duration in hours
    -m : set work duration in minutes
    -s : set work duration in seconds
    -w : set progress bar width in pixels (default: 100)
    *note : use one time arg at a time!"""

avail_args = {'-h': 0, '-m': 0, '-s': 0, '-w': 0, '--help': help_text}
use_args = sys.argv[1:]

try:
    if '--help' in use_args:
        print(avail_args['--help'])
        exit()
    i = 0
    while i < len(use_args):
        if use_args[i] not in avail_args:
            print(f'unknown option: {use_args[i]}\n', help_text)
            exit()
        avail_args[use_args[i]] = use_args[i + 1]
        i += 2
except Exception:
    pass


def get_set_time(args):
    for k, v in args.items():
        if k in ('-h', '-m', '-s') and v:
            if k == '-h':
                return int(v) * 3600
            elif k == '-m':
                return int(v) * 60
            else:
                return int(v)


set_time = get_set_time(avail_args) or 32400
BAR_W = int(avail_args['-w']) if avail_args['-w'] else 100
H = 22


def make_icon(percent):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, BAR_W, H)
    ctx = cairo.Context(surface)

    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()

    fill_w = int(BAR_W * min(percent, 100) / 100)
    ctx.set_source_rgba(1, 1, 1, 0.85)
    ctx.rectangle(0, 3, fill_w, H - 6)
    ctx.fill()

    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.set_line_width(1)
    ctx.rectangle(0.5, 3.5, BAR_W - 1, H - 7)
    ctx.stroke()

    surface.write_to_png(ICON_TMP)
    return ICON_TMP


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        return int(float(f.readline().split()[0]))


def update(ind_app):
    percent = int(get_uptime() / set_time * 100)
    ind_app.set_icon_full(make_icon(percent), f'{percent}%')
    GLib.timeout_add(1000, lambda: update(ind_app))


def quit(source):
    import os
    if os.path.exists(ICON_TMP):
        os.remove(ICON_TMP)
    Gtk.main_quit()


ind_app = appindicator.Indicator.new(
    APPINDICATOR_ID, ICON_TMP,
    appindicator.IndicatorCategory.SYSTEM_SERVICES)
ind_app.set_status(appindicator.IndicatorStatus.ACTIVE)

menu = Gtk.Menu()
menu_item = Gtk.MenuItem(label="Exit")
menu.append(menu_item)
menu_item.connect("activate", quit)
menu_item.show_all()
ind_app.set_menu(menu)

update(ind_app)
Gtk.main()
