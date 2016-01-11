# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:44:45 2016

@author: ethansolomon
"""
import numpy as np
from os.path import *
from ptsa.data.events import Events
from ptsa.data.rawbinwrapper import RawBinWrapper

def get_sub_events(task, sub, eliminate_events_with_no_eeg=True, rhino_prefix='/'):
    """Returns all events for a given task and subject identifier"""    
    from MatlabIO import read_single_matlab_matrix_as_numpy_structured_array
    
    e_path = rhino_prefix+'/data/events/'+task+'/'+sub+'_events.mat'    
    
    # extract matlab matrix (called 'events') as numpy structured array
    struct_array = read_single_matlab_matrix_as_numpy_structured_array(e_path, 'events')

    evs = Events(struct_array)

    if eliminate_events_with_no_eeg:

        # eliminating events that have no eeg file
        indicator = np.empty(len(evs), dtype=bool)
        indicator[:] = False
        for i, ev in enumerate(evs):
            indicator[i] = (type(evs[i].eegfile).__name__.startswith('unicode')) & (len(str(evs[i].eegfile)) > 3)

        #Due to numpy upgrade
        evs = Events(evs[indicator])
    
    evs = evs.add_fields(esrc=np.dtype(RawBinWrapper))

    import pathlib

    for ev in evs:
        try:
            eeg_file_path = join(rhino_prefix, str(pathlib.Path(str(ev.eegfile)).parts[1:]))
            ev.esrc = RawBinWrapper(eeg_file_path)
            #self.raw_data_root=str(eeg_file_path)
        except TypeError:
            print 'skipping event with eegfile=',ev.eegfile
            pass
    
    return(evs)    
    
    
#    from EventReader import EventReader
#    
#    e_path = rhino_prefix+'/data/events/'+task+'/'+sub+'_events.mat'
#    e_reader = EventReader(event_file=e_path, eliminate_events_with_no_eeg=True,
#                          data_dir_prefix=rhino_prefix)
#    
#    e_reader.read()
#    events = e_reader.get_output()
#    
#    return(events)