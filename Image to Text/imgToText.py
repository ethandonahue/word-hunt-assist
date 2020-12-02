import pytesseract
import re
import numpy as np
import cv2
from collections import defaultdict
from PIL import Image, ImageEnhance, ImageFilter, ImageGrab
from itertools import product
import cv2
import win32gui

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)





im = cv2.imread('1.png')

    
im[np.where((im > [50,50,50]).all(axis = 2))] = [255,255,255]
cv2.imwrite('output.png', im)
text = pytesseract.image_to_string(im, lang='hnt', \
        config='--psm 6')


text = ''.join(text.split()).lower()
"""print(text)"""

n = 4
text = [text[i:i+n] for i in range(0, len(text), n)]

grid = text
nrows, ncols = len(grid), len(grid[0])

alphabet = ''.join(set(''.join(grid)))

bogglable = re.compile('[' + alphabet + ']{5,}$', re.I).match

words = set(word.rstrip('\n') for word in open('words.txt') if bogglable(word))

prefixes = set(word[:i] for word in words

for i in list(range(2, len(word)+1)))

def solve():
    for y, row in enumerate(grid):
        for x, letter in enumerate(row):
            for result in extending(letter, ((x, y),)):
                yield result

def extending(prefix, path):
    if prefix in words:
        yield (prefix, path)
    for (nx, ny) in neighbors(path[-1]):
        if (nx, ny) not in path:
            prefix1 = prefix + grid[ny][nx]
            if prefix1 in prefixes:
                for result in extending(prefix1, path + ((nx, ny),)):
                    yield result
                    
def neighbors(p):
    (x, y) = p
    for nx in range(max(0, x-1), min(x+2, ncols)):
        for ny in range(max(0, y-1), min(y+2, nrows)):
            yield (nx, ny)

wordList = '\n'.join(sorted(set(word for (word, path) in solve()), key=len, reverse=True))


print(wordList)
