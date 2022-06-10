# File containing the function loadfile,
# used as an entry point to load different
# AFM data format files.

import os
from .constants import *
from .jpk.loadjpkfile import loadJPKfile
from .nanosc.loadnanoscfile import loadNANOSCfile
from .ar.load_ibw_forcecurve import load_ibw_fc
from .load_uff import loadUFFtxt
from .uff import UFF

def loadfile(filepath):
    """
    Load AFM file. 
    
    Supported formats:
        - JPK --> .jpk-force, .jpk-force-map, .jpk-qi-data
        - NANOSCOPE --> .spm, .pfc
        - ASYLUM RESEARCH --> .ibw
        - UFF --> .uff

            Parameters:
                    filepath (str): Path to the file.
            
            Returns:
                    UFF (uff.UFF): Universal File Format object containing loaded data.
    """
    filesuffix = os.path.splitext(filepath)[-1]

    uffobj = UFF()

    if filesuffix in jpkfiles:
        uffobj = loadJPKfile(filepath, uffobj, filesuffix)
    
    elif filesuffix in nanoscfiles:
        uffobj = loadNANOSCfile(filepath, uffobj)
    
    elif filesuffix in ufffiles:
        uffobj = loadUFFtxt(filepath, uffobj)

    elif filesuffix in ar_exts:
        uffobj = load_ibw_fc(filepath, uffobj)
    
    return uffobj