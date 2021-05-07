# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 10:45:37 2021

@author: jesakke
"""



from pathlib import Path
import logging
import random
import numpy as np


# Global seeds
random.seed(42)
np.random.seed(42)


# Folders
PROJECT_DIR = Path.cwd()
CONFIG_FILE = PROJECT_DIR / 'config.txt'
OUTPUT_DIR  = PROJECT_DIR / 'output'


# input link


