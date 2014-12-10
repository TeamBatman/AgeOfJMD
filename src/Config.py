# LISTE DES CONFIGURATIONS DU JEUX
import os
import sys


SKIP_MENU = False
SKIP_LOADING = False
PLAY_MUSIC = True
DEBUG_VERBOSE = False




# DÉSACTIVATION DU PRINTAGE
if not DEBUG_VERBOSE:
    sys.stdout = open(os.devnull, 'w')
