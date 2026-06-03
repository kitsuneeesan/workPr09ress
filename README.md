# workPr09ress

A minimal work progress bar in the Ubuntu system tray indicator. Shows how far along you are in your workday based on system uptime.

## Requirements

```bash
sudo apt install gir1.2-appindicator3-0.1 python3-cairo
```

## Usage

```bash
python3 main.py              # default 9 hours
python3 main.py -h 8         # 8 hour workday
python3 main.py -m 30        # 30 minute session
python3 main.py -s 3600      # 3600 seconds
python3 main.py -w 150       # custom bar width (px), default 100
python3 main.py -h 8 -w 120  # combine args
python3 main.py --help
```

## Notes

- Progress is based on system uptime, so it assumes you boot up when you start working.
- Tested on Ubuntu 24.04 with GNOME. Requires the **AppIndicator and KStatusNotifierItem Support** GNOME extension to be enabled.
