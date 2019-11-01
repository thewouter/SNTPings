import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import ciede2000
import json
import random

remoteStart = [1500, 700]

xstart = 508
ystart = 500
xend = 800
yend = 800
xpixels = 100
ypixels = 100

refim = cv2.imread("reference.png")

ypixels, xpixels, useless = refim.shape

#os.system("import -window root -crop {}x{}+{}+{} temp.png".format(str(xend-xstart), str(yend-ystart), str(xstart),
#                                                                  str(ystart)))
im = cv2.imread("temp.png")
nx = np.linspace(0, xend-xstart-1, xpixels)
ny = np.linspace(0, yend-ystart-1, ypixels)

nx = np.round(nx)
ny = np.round(ny)

gridx, gridy = np.meshgrid(nx, ny)

rescaled = im[gridy.astype(int), gridx.astype(int)]

diff = np.zeros((xpixels, ypixels))

toUpdate = {'start': remoteStart, 'pixels': {}}

for x in range(xpixels):
    for y in range(ypixels):
        if refim[y, x, 0] == 110 and refim[y, x, 1] == 0 and refim[y, x, 2] == 255:
            continue
        val = ciede2000.ciede2000(ciede2000.rgb2lab(refim[y, x]), ciede2000.rgb2lab(rescaled[y, x]))
        if val > 1:
            toUpdate['pixels']["{},{}".format(x, y)] = refim[y, x].tolist()


# Shuffle updateables?

with open('updateable.json', 'w') as fp:
    json.dump(toUpdate, fp)
