# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 18:14:18 2016

@author: ethansolomon
"""

import os
from mayavi.core.api import Engine
from mayavi.sources.vtk_file_reader import VTKFileReader
from mayavi.modules.surface import Surface

vtkFile_l = 'lh.vtk'
vtkFile_r = 'rh.vtk'

# Create the MayaVi engine and start it.
engine = Engine()
engine.start()
scene = engine.new_scene()

# Read in VTK file and add as source
reader1 = VTKFileReader()
reader1.initialize(vtkFile_l)
engine.add_source(reader1)

reader2 = VTKFileReader()
reader2.initialize(vtkFile_r)
engine.add_source(reader2)

# Add Surface Module
surface = Surface()
engine.add_module(surface)

# Move the camera
scene.scene.camera.elevation(-70)

# Save scene to image file
scene.scene.save_png('image.png')

# Create a GUI instance and start the event loop.
# This stops the window from closing
from pyface.api import GUI
gui = GUI()
gui.start_event_loop()