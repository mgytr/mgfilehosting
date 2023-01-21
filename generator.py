from os import listdir, chdir, mkdir
from string import ascii_letters
from random import choice
from sys import platform
chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def get_path(*path):
    if platform == 'win32':
        _path = '\\'.join(path)
    else:
        _path = '/'.join(path)
    return _path


for i in ascii_letters:
    chars.append(i)
def create_link(length=5):
    code = ''
    for x in range(length):
        code += choice(chars)
    for x in listdir('links'):
        if code == x: create_link(length)
    mkdir(get_path('links', code))
    return code

