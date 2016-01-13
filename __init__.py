# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:30:01 2016

@author: ethansolomon
"""

import numpy as np
from os.path import *
from ptsa.data.events import Events
from ptsa.data.rawbinwrapper import RawBinWrapper

def get_sub_events(task, sub, eliminate_events_with_no_eeg=True, rhino_prefix='/', ignore_no_params=False):
    """Returns all events for a given task and subject identifier

    Keyword arguments:
    task -- string of task name
    sub -- string of subject identifier
    eliminate_events_with_no_eeg -- (default: True) Do not return events for which no corresponding eeg file exists.
    rhino_prefix -- (default: '/') To get data if rhino is mounted as an external volume from a local computer.
    ignore_no_params -- (default: False) Automatically handles IOError when no params.txt file is found for a subject.

    """
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

    #This may throw and error for a few subjects who have no params file. Should be written to handle this elegantly.

    if ignore_no_params:
        try:
            for ev in evs:
                try:
                    eeg_file_path = join(rhino_prefix, str(pathlib.Path(str(ev.eegfile)).parts[1:]))
                    ev.esrc = RawBinWrapper(eeg_file_path)
                    #self.raw_data_root=str(eeg_file_path)
                except TypeError:
                    print 'skipping event with eegfile=',ev.eegfile
                    pass
        except IOError:
            print('No params.txt or .params file found for '+sub)

    else:
        for ev in evs:
            try:
                eeg_file_path = join(rhino_prefix, str(pathlib.Path(str(ev.eegfile)).parts[1:]))
                ev.esrc = RawBinWrapper(eeg_file_path)
                #self.raw_data_root=str(eeg_file_path)
            except TypeError:
                print 'skipping event with eegfile=',ev.eegfile
                pass

    return(evs)
    
    
def get_bp_tal_data(sub, rhino_prefix='/'):
    from get_bipolar_subj_elecs import get_bipolar_subj_elecs
    
    subjpath = rhino_prefix+'/data/eeg/'+sub
    
    return(get_bipolar_subj_elecs(subjpath))
    

def get_all_subs(taskname, rhino_prefix='/'):
    from glob import glob
    
    fns = glob(rhino_prefix+'/data/events/'+taskname+'/*_events.mat')
    subs = [s.split('/')[-1].split('_e')[0] for s in fns]
    
    return(subs)
    
def get_mtl_leads():
    pass
    
def get_hipp_elecs():
    pass