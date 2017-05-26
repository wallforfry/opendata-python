"""
Project : OpenData-python
File : main.py
Author : DELEVACQ Wallerand && COHEN Johana
Date : 28/03/2017
"""
import os, sys
from ihm import launch_gui
progname = os.path.basename(sys.argv[0])
progversion = "1.0"

if __name__ == "__main__":
    print("Application launching")
    launch_gui()