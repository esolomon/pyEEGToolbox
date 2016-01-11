# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:44:43 2016

@author: ethansolomon
"""

def get_all_subs(taskname, rhino_prefix='/'):
    from glob import glob
    
    fns = glob(rhino_prefix+'/data/events/'+taskname+'/*_events.mat')
    subs = [s.split('/')[-1].split('_e')[0] for s in fns]
    
    return(subs)