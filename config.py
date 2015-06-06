"""

Some secret fun times for AVENTUREGAME

This file is filled with sneaky, confusing things to confound people who are trying to guess the cheat codes.

Good luck, cheaters.

"""

from items_lists import random_weapon
import hashlib

def config():
    if confus(unconfus('bob')) == 'bob':
        print '<secrets configured successfully>'

def confus(b):
    return ''.join([chr(a-17) for a in b])

def unconfus(a):
    return [ord(b)+17 for b in a]


if __name__ != '__main__':

    config0 = [126, 118, 131, 125, 122, 127, 131, 128, 115, 128, 133]
    config1 = random_weapon(confus([115, 128, 132, 132, 112, 136, 118, 114, 129, 128, 127, 132]))
    config2 = [129, 125, 114, 116, 122, 117, 128]
    config3 = [128, 138, 238, 119, 111]
    config4 = [132, 122, 137, 129, 114, 116, 124, 133, 128, 120, 128]
    config5 = [123, 112, 147, 117, 118, 192, 123, 128]

    ha0 = 'b6fe35296e44d8d2955ef7f609f90904'
    ha1 = ''

    ha2 = '75b3adc3bb2a0dcd9e309612c3cedcff'
    ha3 = '76a61453ff19529bd4f230b688f1f416'


if __name__ == '__main__':

    config()
    for i in range(1):
        print hashlib.md5(raw_input()).hexdigest()
