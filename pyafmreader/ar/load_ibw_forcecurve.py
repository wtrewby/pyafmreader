"""
Loading Asylum Research IBW force curves into memory and converting 

@author: WJT
@date: 2022-06-10
"""
import os
import numpy as np

from igor import binarywave
from .get_metadata import read_note, get_chan_labels, get_force_curve_segments

from ..importutils import ForceCurve, Segment
from ..constants import ar_exts
from ..uff import UFF

def load_ibw_fc(path:str, uff:UFF):
    """
    Parsing binary IBW data with metadata into UFF format
    Parameters
    ----------
        path : str
            Full path to force curve, appropriately formatted for OS
        uff : UFF
            UFF object in which force curve data will be stored
    Returns
    -------
        uff : UFF
            Loaded force curve object
    """
    assert os.path.isfile(path), "Path passed is not a valid file: {}".format(path)
    assert os.path.splitext(path)[-1] in ar_exts, "Path does not contain a valid Asylum Research extension: {}".format(path)

    raw_ibw = binarywave.load(path)["wave"]

    # Parse metadata
    header = raw_ibw["wave_header"]
    fc_name = header["bname"].decode()
    wave_note = read_note(raw_ibw)

    # Grab channel info
    channel_names, channel_units = get_chan_labels(raw_ibw)

    wave_data = raw_ibw["wData"]
    assert wave_data.shape[-1] == len(channel_names), "Issue with parsing labels of dimensions of wave {}".format(fc_name)
    segments = get_force_curve_segments(wave_note)