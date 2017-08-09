'''
V wps, a 5 cm per second desktop wallpaper generator for windows

edit `MONITORS` near the top of the script to configure the app

Each top level array is a monitor, in the format [x_offset, y_offset, width, height]

To find your offsets, take a screenshot of your desktop and place it in an image
editor, the top left pixel coordinates of each monitor are your offsets.

Width and Height are your monitor resolutions

If you need to, edit the monitor resolution RES to match the resolution of your file

If you need to, edit the `SECONDS_OFFSET` to remove seconds from the start of the file

If you need to, edit the `MINUTES_END` to mark the minutes after which the movie ends

If you need to, edit the `SECONDS_END` to mark the seconds after the final minute which
the movie ends
'''

import os
import random
import ctypes

MONITORS = [
    [0, 220, 1600, 900],
    [1600, 157, 1920, 1080],
    [3520, 0, 1280, 1024]
]
RES = [1920, 1078]
SECONDS_OFFSET = 13
MINUTES_END = 50
SECONDS_END = 59

for n in range(0, len(MONITORS)):
    random_number = random.randrange(SECONDS_OFFSET, MINUTES_END * 60 + SECONDS_END)
    htime = 0
    mtime = random_number // 60
    stime = random_number % 60

    os.system('ffmpeg -ss {:02d}:{:02d}:{:02d} -i 5cmps.mkv -vframes 1 {:02d}.png -y'.format(
        htime,
        mtime,
        stime,
        n
    ))

    xscale = 0
    yscale = 0

    if MONITORS[n][2] / MONITORS[n][3] > RES[0] / RES[1]:
        yscale = -1
        xscale = MONITORS[n][2]
    else:
        xscale = -1
        yscale = MONITORS[n][3]

    os.system('ffmpeg -i {0:02d}.png -vf scale={1}:{2} {0:02d}.png -y'.format(
        n,
        xscale,
        yscale
    ))
    os.system('ffmpeg -i {0:02d}.png -filter:v "crop={1}:{2}" {0:02d}.png -y'.format(
        n,
        MONITORS[n][2],
        MONITORS[n][3]
    ))
    os.system('ffmpeg -i {0:02d}.png -vf "pad=width={1}:height={2}:x={3}:y={4}:color=black" {0:02d}.png -y'.format(
        n,
        MONITORS[n][2],
        1237,
        0,
        MONITORS[n][1]
    ))

for n in range(0, len(MONITORS) - 1):
    os.system('ffmpeg -i {0:02d}.png -i {1:02d}.png -filter_complex hstack {1:02d}.png -y'.format(
        n,
        n + 1
    ))

for n in range(0, len(MONITORS) - 1):
    os.system("del {0:02d}.png".format(n))

ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.join(os.getcwd(), '{:02d}.png'.format(len(MONITORS) - 1)), 1)