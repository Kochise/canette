#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_view_flex.py
	Flexx view
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# External libraries (installed with pip, conda, setup.py, ...)

import numpy as np

# python3 -m pip install --upgrade bokeh
from bokeh.plotting import figure

# python3 -m pip install --upgrade pygame
# python3 -m pip install --upgrade flexx
from flexx import app
from flexx import event
from flexx import flx
from flexx import ui

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_enum import CANP_ENUM__HEAD_MAIN

from canp_enum import CANP_ENUM__IDX_X_CAN
from canp_enum import CANP_ENUM__IDX_X_REF
from canp_enum import CANP_ENUM__IDX_Y_CAN
from canp_enum import CANP_ENUM__IDX_Y_REF
from canp_enum import CANP_ENUM__IDX_Z_CAN
from canp_enum import CANP_ENUM__IDX_Z_REF

#  --- GLOBAL ---

# Local settings (might be present in other files yet with different values)

#  --- CLASS ---

# Plot 1
N = 1000
x = np.random.normal(0, np.pi, N)
y = np.sin(x) + np.random.normal(0, 0.2, N)
TOOLS = "pan,wheel_zoom,box_zoom,reset,box_select"
p1 = figure(tools=TOOLS)
p1.scatter(x, y, alpha=0.1, nonselection_alpha=0.1)

# Plot2
t = np.linspace(0, 6.5, 100)
p2 = figure(tools=TOOLS, sizing_mode='scale_width')
p2.line(t, np.sin(t))
p3 = figure(tools=TOOLS, sizing_mode='scale_width')
p3.line(t, np.cos(t))

class BokehExample(flx.PyComponent):

	def init(self):
		with flx.HSplit(minsize=300) as self.widget:
			self.plot1 = flx.BokehWidget.from_plot(p1, title='Scatter')
			with flx.VFix(title='Sine'):
				Controls()
				with flx.Widget(style='overflow-y:auto;', flex=1):
					self.plot2 = flx.BokehWidget.from_plot(p2)
					self.plot3 = flx.BokehWidget.from_plot(p3)


class Controls(flx.FormLayout):
	def init(self):
		self.amp = flx.Slider(title='Amplitude', max=2, value=1)
		self.freq = flx.Slider(title='Frequency', max=10, value=5)
		self.phase = flx.Slider(title='Phase', max=3, value=1)

	@flx.reaction
	def _update_sine(self):
		global window
		amp, freq, phase = self.amp.value, self.freq.value, self.phase.value
		# Get reference to data source
		ds = None
		plot2 = self.parent.children[1].children[0]
		plot = plot2.plot
		if plot:
			for ren in plot.model.renderers.values():
				if ren.data_source:
					ds = ren.data_source
					break

		# Update
		if ds:
			ds.data.y = [amp*window.Math.sin(x*freq+phase) for x in ds.data.x]
			ds.change.emit()  # or trigger('change') in older versions

class canp_view_flexx:
	""" CAN view
	"""

	@staticmethod
	def display(
				i_list_farr,	# all the lists in one package
				i_int_tmp,		# time index
				i_int_pos,		# pos index
			) -> None:
		# Display data in Flexx windows
		m = flx.launch(BokehExample, 'app')
		flx.run()

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	if True:
		pass
	else:
		pass

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
