"""
Functions for extracting metadata from IBW files that have already been loaded into memory
"""
import numpy as np

def read_note(raw_ibw:dict, codec:str='utf-8')->dict:
    """
    Parses the IBW wave parameters and returns as a dict
    Parameters
    ----------
        raw_ibw : dict
            Raw wave info and data from IBW file
        codec : str, optional
            Codec to be used to decode the bytestrings into Python strings if needed.
            Default 'utf-8'
    Returns
    -------
        parm_dict : dictionary
            Dictionary containing parameters
    """
    binary_note = raw_ibw["note"]
    if type(binary_note) == bytes:
        try:
            binary_note = binary_note.decode(codec)
        except:
            binary_note = binary_note.decode("ISO-8859-1")  # for older AR software
    binary_note = binary_note.rstrip("\r")
    parm_list = binary_note.split("\r")
    parm_dict = dict()
    for pair_string in parm_list:
        temp = pair_string.split(":")
        if len(temp) == 2:
            temp = [item.strip() for item in temp]
            try:
                num = float(temp[1])
                parm_dict[temp[0]] = num
                try:
                    if num == int(num):
                        parm_dict[temp[0]] = int(num)
                except OverflowError:
                    pass
            except ValueError:
                parm_dict[temp[0]] = temp[1]

    # Grab the creation and modification times:
    other_parms = raw_ibw["wave_header"]
    for key in ["creationDate", "modDate"]:
        try:
            parm_dict[key] = other_parms[key]
        except KeyError:
            pass

    return parm_dict
    
def get_chan_labels(raw_ibw, codec='utf-8'):
    """
    Retrieves the names of the data channels and default units
    Parameters
    ----------
    raw_ibw : dict
            Raw wave info and data from IBW file
    codec : str, optional
        Codec to be used to decode the bytestrings into Python strings if needed.
        Default 'utf-8'
    Returns
    -------
    labels : list of strings
        List of the names of the data channels
    default_units : list of strings
        List of units for the measurement in each channel
    """
    temp = raw_ibw["labels"]
    binary_labels = []
    for item in temp:
        if len(item) > 0:
            binary_labels += item
    labels = [item.decode() for item in binary_labels]
    for item in labels:
        if item == '':
            labels.remove(item)

    default_units = []
    for chan_ind, chan in enumerate(labels):
        # clean up channel names
        if type(chan) == bytes:
            chan = chan.decode(codec)
        # if chan.lower().rfind('trace') > 0:
        #     labels[chan_ind] = chan[:chan.lower().rfind('trace') + 5]
        else:
            labels[chan_ind] = chan
        # Figure out (default) units
        if chan.startswith('Phase'):
            default_units.append('deg')
        elif chan.startswith('Current'):
            default_units.append('A')
        elif "volt" in chan.lower() or chan in ["In0", "In1", "In2", "BPk0", "BPk1", "BPk2"]:
            default_units.append("V")
        elif "time" in chan.lower():
            default_units.append("s")
        else:
            default_units.append('m')

    return labels, default_units

def get_force_curve_segments(wave_note:dict)->dict:
    """
    Generates a dictionary that can be used to split force curve into extension/retraction data and dwells where appropriate 

    Parameters
    ----------
        wave_note : dict
            The parsed note from the IBW file, detailing settings and
            parameters.
    Returns
    -------
        segments : dictionary
            contains keys "ext", "ret", "dwell_toward" and "dwell_away" These keys point to length-2 lists 
            with the indices where each segment begins and ends
    """
    # Indices in note correspond to split points; directions correspond to type: 1=extension; -1=retraction; 0=dwell
    segment_indices = [int(index) for index in wave_note["Indexes"].split(',')]
    segment_directions = wave_note["Direction"].split(',')
    direction_types = {
        "1": "ext",
        "-1": "ret",
        "0": "dwell",
        "NaN": np.nan
    }

    segments = {
        "ext": (None, None),
        "ret": (None, None),
        "dwell_towards": (None, None),
        "dwell_away": (None, None)
    }
    for i, segment_index in enumerate(segment_indices):
        if i == 0:
            # First index is always zero, with direction=NaN
            pass
        else:
            start = segment_indices[i-1]
            end = segment_index
            seg_type = direction_types[segment_directions[i]]
            # Try to work out which sort of dwell we have by checking what the previous segment type was
            if seg_type == "dwell":
                if segment_directions[i-1] == "1":
                    seg_type = "dwell_towards"
                elif segment_directions[i-1] == "-1":
                    seg_type = "dwell_away"
            
            segments[seg_type] = (start, end)
    
    return segments