# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:44:45 2016

@author: ethansolomon
"""

def get_bp_tal_data(sub, rhino_prefix='/'):
    from get_bipolar_subj_elecs import get_bipolar_subj_elecs
    
    subjpath = rhino_prefix+'/data/eeg/'+sub
    
    return(get_bipolar_subj_elecs(subjpath))