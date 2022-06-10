# File containing constants used in the package.

# File extensions of files supported by this library
jpkfiles = ('.jpk-force', '.jpk-force-map', '.jpk-qi-data')     # As in 26-04-2022
nanoscfiles = ('.spm', '.pfc')                                  # As in 26-04-2022
ufffiles = ('.uff')                                             # As in 26-04-2022
ar_exts = (".ibw")

# Default values for UFF (Universal File Format) files.
UFF_code = '_1_2_3_4_5'                                         # Default UFF code for V.x.x.x
UFF_version = '0'                                               # Default UFF version for V.x.x.x

# Defaults values for JPK file headers.
default_angle = 0                                               # in degrees
default_delay = 0                                               # in seconds
multiplier_default = 1                                          # no units
offset_default = 0                                              # no units
boolean_default = 'false'                                       # no units
num_segments_default = 2                                        # no units, asume approach-retract
scaling_factor = 1e9                                            # nanometer --> meter

# Hard coded values for JPK and Nanoscope files.
JPK_SETPOINT_MODE = 'Relative'                                  # JPK setpoint mode is always relative.                                           