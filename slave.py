from multiping import MultiPing
import json
import random
import time

base = '2001:610:1908:a000:{}:{}:{}{}:{}{}'


def to_hex(i, length=2):
    return str(format(int(i), '0{}x'.format(length)))


running = True

while running:
    updates = []
    print("updating tiles")
    with open('updateable.json') as file:
        data = json.load(file)
        start = data['start']
        pixels = data['pixels']

        for key in pixels:
            coord = key.split(',')
            rgb = pixels[key]
            coord.extend(rgb)
            updates.append(coord)

    index = random.randint(0, len(updates)-1)

    startTime = time.time()
    while time.time() - startTime < 30:
        data = updates[index]
        x = int(data[0]) + int(start[0])
        y = int(data[1]) + int(start[1])
        r = data[2]
        g = data[3]
        b = data[4]
        opacity = 255;
        ping = MultiPing([base.format(to_hex(x, 4), to_hex(y, 4), to_hex(r), to_hex(g), to_hex(b), to_hex(opacity))])
        ping.send()
        index = (index + 1) % len(updates)
