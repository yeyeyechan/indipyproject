'''



'''

# -*- coding: utf-8 -*-
import sys
sys.path.append("C:\\dev\\indiPyProject\\log")
sys.path.append("C:\\dev\\indiPyProject\\process")
sys.path.append("C:\\dev\\indiPyProject\\data")
sys.path.append("C:\\dev\\indiPyProject\\analysis")
sys.path.append("C:\\dev\\indiPyProject")
sys.path.append("C:\\dev\\indiPyProject\\pyflask")
import subprocess


if __name__ == "__main__":
    #print( sys.argv[1])
    subprocess.call(['sudo', 'python', 'C:\\dev\\indiPyProject\\data\\TR_1314_3.py', sys.argv[1]])
    subprocess.call(['sudo', 'python', 'C:\\dev\\indiPyProject\\data\\TR_1206.py', sys.argv[1]])

